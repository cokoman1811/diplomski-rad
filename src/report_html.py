"""Generate an HTML report viewer for experiment results and figures."""

from __future__ import annotations

import html
import os
import re
import sys
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd

from .analysis import best_method_per_factor, build_method_leaderboard
from .config import ALL_METHODS
from .method_info import METHOD_DESCRIPTIONS
from .paths import FIGURES_DIR, PROJECT_ROOT, RESULTS_DIR, TABLES_DIR, ensure_project_dirs

REPORT_PATH = RESULTS_DIR / "report.html"

_CATEGORY_RULES: list[tuple[str, str]] = [
    (r"^reconstruction_", "Rekonstrukcija"),
    (r"^bar_", "Usporedba (bar chart)"),
    (r"^heatmap_", "Heatmap"),
    (r"^boxplot_", "Boxplot grešaka"),
    (r"^error_by_hour_", "Greška po satu"),
    (r"^error_by_month_", "Greška po mjesecu"),
    (r"^error_by_weekday_", "Greška po danu"),
    (r"^error_by_season_", "Greška po sezoni"),
    (r"^scatter_", "Scatter residuala"),
    (r"^hist_", "Histogram grešaka"),
    (r"^ranking_", "Rang metoda"),
    (r"^lines_", "Linijski pregled"),
]


@dataclass
class FigureEntry:
    """Metadata for one saved figure."""

    filename: str
    title: str
    category: str
    factor: str
    method: str
    rel_path: str


def _method_label(method: str) -> str:
    """Return readable method name."""
    if not method:
        return "Sve metode"
    return METHOD_DESCRIPTIONS.get(method, {}).get("name", method)


def _classify_figure(stem: str) -> str:
    """Map filename stem to a human-readable category."""
    for pattern, label in _CATEGORY_RULES:
        if re.search(pattern, stem):
            return label
    return "Ostalo"


def _parse_figure_metadata(filename: str) -> tuple[str, str, str]:
    """Extract category, factor and method from a figure filename."""
    stem = Path(filename).stem
    category = _classify_figure(stem)

    factor = ""
    method = ""

    match = re.search(r"factor_(\d+)_([a-z_]+)$", stem)
    if match:
        factor = match.group(1)
        method = match.group(2)
    else:
        match = re.search(r"factor_(\d+)$", stem)
        if match:
            factor = match.group(1)

    if stem.startswith("bar_") or stem.startswith("heatmap_") or stem.startswith("lines_"):
        metric = stem.split("_", 1)[1]
        return category, "", metric.upper()

    title_parts = [category]
    if factor:
        title_parts.append(f"faktor {factor}")
    if method:
        title_parts.append(_method_label(method))
    return category, factor, method


def collect_figure_entries(figures_dir: Path | None = None) -> list[FigureEntry]:
    """Collect metadata for all PNG figures."""
    figures_dir = figures_dir or FIGURES_DIR
    if not figures_dir.exists():
        return []

    entries: list[FigureEntry] = []
    for path in sorted(figures_dir.glob("*.png")):
        category, factor, method = _parse_figure_metadata(path.name)
        title_parts = [category]
        if factor:
            title_parts.append(f"faktor {factor}")
        if method and not method.isupper():
            title_parts.append(_method_label(method))
        elif method:
            title_parts.append(method)

        entries.append(FigureEntry(
            filename=path.name,
            title=" · ".join(title_parts),
            category=category,
            factor=factor,
            method=method,
            rel_path=f"figures/{path.name}",
        ))
    return entries


def _results_table_html(results: pd.DataFrame) -> str:
    """Render results dataframe as an HTML table."""
    if results.empty:
        return "<p>Nema rezultata.</p>"

    display = results.copy()
    display["method"] = display["method"].map(_method_label)
    display = display.sort_values(["factor", "mae"])
    display["factor"] = display["factor"].astype(int)
    for column in ("mae", "rmse", "r2"):
        display[column] = display[column].map(lambda value: f"{value:.4f}")

    return display.to_html(index=False, classes="data-table", border=0)


def _best_methods_html(results: pd.DataFrame) -> str:
    """Render best-method cards."""
    best = best_method_per_factor(results)
    cards = []
    for _, row in best.iterrows():
        cards.append(
            f'<div class="card">'
            f'<div class="card-label">Faktor {int(row["factor"])}</div>'
            f'<div class="card-title">{html.escape(_method_label(row["method"]))}</div>'
            f'<div class="card-meta">MAE {row["mae"]:.4f} · RMSE {row["rmse"]:.4f} · '
            f'R² {row["r2"]:.4f}</div>'
            f"</div>"
        )
    return "\n".join(cards)


def _leaderboard_html(results: pd.DataFrame) -> str:
    """Render leaderboard rows."""
    leaderboard = build_method_leaderboard(results).head(7)
    mean_mae = results.groupby("method")["mae"].mean()
    rows = []
    for rank, (_, row) in enumerate(leaderboard.iterrows(), start=1):
        rows.append(
            "<tr>"
            f"<td>{rank}</td>"
            f"<td>{html.escape(_method_label(row['method']))}</td>"
            f"<td>{row['average_rank']:.2f}</td>"
            f"<td>{mean_mae[row['method']]:.4f}</td>"
            "</tr>"
        )
    return "\n".join(rows)


def _table_links_html() -> str:
    """Render links to CSV tables."""
    if not TABLES_DIR.exists():
        return ""

    links = []
    for path in sorted(TABLES_DIR.glob("*.csv")):
        rel = path.relative_to(RESULTS_DIR).as_posix()
        links.append(
            f'<li><a href="{html.escape(rel)}" target="_blank">{html.escape(path.name)}</a></li>'
        )
    return "\n".join(links)


def _figure_card_html(entry: FigureEntry) -> str:
    """Render one figure card."""
    return (
        f'<article class="figure-card" '
        f'data-category="{html.escape(entry.category)}" '
        f'data-factor="{html.escape(entry.factor)}" '
        f'data-method="{html.escape(entry.method)}">'
        f'<div class="figure-media">'
        f'<img src="{html.escape(entry.rel_path)}" alt="{html.escape(entry.title)}" loading="lazy">'
        f"</div>"
        f'<div class="figure-caption">{html.escape(entry.title)}</div>'
        f"</article>"
    )


def _group_entries_by_method(entries: list[FigureEntry]) -> list[tuple[str, str, list[FigureEntry]]]:
    """Split figure entries into ordered method sections."""
    by_method: dict[str, list[FigureEntry]] = {method: [] for method in ALL_METHODS}
    global_entries: list[FigureEntry] = []

    for entry in entries:
        if entry.method in METHOD_DESCRIPTIONS:
            by_method[entry.method].append(entry)
        else:
            global_entries.append(entry)

    sections: list[tuple[str, str, list[FigureEntry]]] = []

    for method in ALL_METHODS:
        method_entries = by_method[method]
        if not method_entries:
            continue
        method_entries.sort(key=lambda item: (int(item.factor or 0), item.category, item.filename))
        info = METHOD_DESCRIPTIONS[method]
        subtitle = info.get("description", "")
        sections.append((method, subtitle, method_entries))

    if global_entries:
        global_entries.sort(key=lambda item: (item.category, int(item.factor or 0), item.filename))
        sections.append(
            (
                "__global__",
                "Usporedbe i grafikoni koji prikazuju sve metode odjednom.",
                global_entries,
            )
        )

    return sections


def _figure_gallery_sections_html(entries: list[FigureEntry]) -> str:
    """Render gallery grouped by method with section headings."""
    if not entries:
        return '<p class="muted">Nema grafikona. Pokreni eksperiment s grafikonima (bez --no-plots).</p>'

    sections_html = []
    for method_key, subtitle, method_entries in _group_entries_by_method(entries):
        if method_key == "__global__":
            heading = "Usporedbe svih metoda"
            section_method = ""
        else:
            heading = _method_label(method_key)
            section_method = method_key

        cards = "\n".join(_figure_card_html(entry) for entry in method_entries)
        count = len(method_entries)
        sections_html.append(
            f'<div class="method-section" data-section-method="{html.escape(section_method)}">'
            f'<div class="method-heading">'
            f'<h3>{html.escape(heading)}</h3>'
            f'<p class="method-subtitle">{html.escape(subtitle)}</p>'
            f'<span class="method-count">{count} grafikona</span>'
            f"</div>"
            f'<div class="gallery">{cards}</div>'
            f"</div>"
        )

    return "\n".join(sections_html)


def _filter_options(values: list[str], label: str) -> str:
    """Build select options for filters."""
    options = [f'<option value="">{label}</option>']
    for value in sorted(values, key=lambda item: (item.isdigit(), item)):
        if not value:
            continue
        display = _method_label(value) if value in METHOD_DESCRIPTIONS else value
        options.append(f'<option value="{html.escape(value)}">{html.escape(display)}</option>')
    return "\n".join(options)


def generate_html_report(
    results: pd.DataFrame,
    output_path: Path | None = None,
    figures_dir: Path | None = None,
) -> Path:
    """Build the HTML report file and return its path."""
    ensure_project_dirs()
    output_path = output_path or REPORT_PATH
    entries = collect_figure_entries(figures_dir)

    factors = sorted({entry.factor for entry in entries if entry.factor}, key=int)
    methods = sorted({entry.method for entry in entries if entry.method and entry.method in METHOD_DESCRIPTIONS})
    categories = sorted({entry.category for entry in entries})

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    figure_count = len(entries)
    run_count = len(results)

    content = f"""<!DOCTYPE html>
<html lang="hr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rezultati eksperimenta — interpolacija vremenskih serija</title>
  <style>
    :root {{
      --bg: #0f1419;
      --panel: #1a2332;
      --panel-2: #243044;
      --text: #e7ecf3;
      --muted: #9aa8bc;
      --accent: #4da3ff;
      --accent-2: #7c5cff;
      --good: #3ddc97;
      --border: #2f3d52;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: linear-gradient(180deg, #0b1017 0%, var(--bg) 100%);
      color: var(--text);
      line-height: 1.5;
    }}
    header {{
      padding: 2rem 1.5rem 1rem;
      border-bottom: 1px solid var(--border);
      background: var(--panel);
    }}
    header h1 {{
      margin: 0 0 0.25rem;
      font-size: 1.6rem;
    }}
    header p {{
      margin: 0;
      color: var(--muted);
    }}
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 1.5rem;
    }}
    section {{
      margin-bottom: 2rem;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.25rem;
    }}
    section h2 {{
      margin: 0 0 1rem;
      font-size: 1.15rem;
      color: var(--accent);
    }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
    }}
    .card {{
      background: var(--panel-2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem;
    }}
    .card-label {{ color: var(--muted); font-size: 0.85rem; }}
    .card-title {{ font-size: 1.05rem; font-weight: 600; margin: 0.35rem 0; }}
    .card-meta {{ color: var(--good); font-size: 0.9rem; }}
    .filters {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      align-items: end;
    }}
    label {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      font-size: 0.85rem;
      color: var(--muted);
    }}
    select, button {{
      background: var(--panel-2);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 0.55rem 0.75rem;
      min-width: 180px;
    }}
    button {{
      cursor: pointer;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      border: none;
      font-weight: 600;
    }}
    .gallery {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.25rem;
      align-items: stretch;
    }}
    .method-section {{
      margin-top: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
    }}
    .method-section:first-of-type {{
      margin-top: 1rem;
      padding-top: 0;
      border-top: none;
    }}
    .method-section.hidden {{ display: none; }}
    .method-heading {{
      margin-bottom: 1rem;
      padding: 1rem 1.1rem;
      background: linear-gradient(135deg, rgba(77, 163, 255, 0.12), rgba(124, 92, 255, 0.10));
      border: 1px solid var(--border);
      border-radius: 12px;
    }}
    .method-heading h3 {{
      margin: 0 0 0.35rem;
      font-size: 1.25rem;
      color: var(--text);
    }}
    .method-subtitle {{
      margin: 0;
      color: var(--muted);
      font-size: 0.92rem;
      max-width: 900px;
    }}
    .method-count {{
      display: inline-block;
      margin-top: 0.65rem;
      padding: 0.2rem 0.55rem;
      border-radius: 999px;
      background: var(--panel-2);
      color: var(--good);
      font-size: 0.8rem;
      border: 1px solid var(--border);
    }}
    .figure-card {{
      background: var(--panel-2);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 100%;
    }}
    .figure-card.hidden {{ display: none; }}
    .figure-media {{
      height: 280px;
      min-height: 280px;
      max-height: 280px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #fff;
      padding: 0.65rem;
      border-bottom: 1px solid var(--border);
    }}
    .figure-card img {{
      display: block;
      max-width: 100%;
      max-height: 100%;
      width: auto;
      height: auto;
      object-fit: contain;
    }}
    .figure-caption {{
      padding: 0.75rem 0.9rem;
      font-size: 0.9rem;
      min-height: 3.25rem;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.92rem;
    }}
    .data-table th, .data-table td {{
      border-bottom: 1px solid var(--border);
      padding: 0.55rem 0.65rem;
      text-align: left;
    }}
    .data-table th {{
      color: var(--accent);
      position: sticky;
      top: 0;
      background: var(--panel);
    }}
    .table-wrap {{ overflow-x: auto; }}
    .leaderboard {{
      width: 100%;
      border-collapse: collapse;
    }}
    .leaderboard th, .leaderboard td {{
      border-bottom: 1px solid var(--border);
      padding: 0.55rem 0.65rem;
      text-align: left;
    }}
    .links {{ columns: 2; column-gap: 2rem; list-style: none; padding: 0; margin: 0; }}
    .links li {{ break-inside: avoid; margin-bottom: 0.35rem; }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .muted {{ color: var(--muted); }}
    .stats {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-top: 0.75rem;
    }}
    .stat {{
      background: var(--panel-2);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      min-width: 140px;
    }}
    .stat-value {{ font-size: 1.3rem; font-weight: 700; color: var(--good); }}
    .stat-label {{ color: var(--muted); font-size: 0.85rem; }}
  </style>
</head>
<body>
  <header>
    <h1>Rezultati eksperimenta</h1>
    <p>Interpolacija temperature · Jena Climate · generirano {html.escape(generated_at)}</p>
    <div class="stats">
      <div class="stat"><div class="stat-value">{run_count}</div><div class="stat-label">pokretanja</div></div>
      <div class="stat"><div class="stat-value">{figure_count}</div><div class="stat-label">grafikona</div></div>
      <div class="stat"><div class="stat-value">{len(factors) or len(results['factor'].unique())}</div><div class="stat-label">faktora</div></div>
    </div>
  </header>

  <main>
    <section>
      <h2>Najbolje metode po faktoru degradacije</h2>
      <div class="cards">{_best_methods_html(results)}</div>
    </section>

    <section>
      <h2>Leaderboard</h2>
      <table class="leaderboard">
        <thead>
          <tr><th>#</th><th>Metoda</th><th>Prosjek ranga</th><th>Prosjek MAE</th></tr>
        </thead>
        <tbody>{_leaderboard_html(results)}</tbody>
      </table>
    </section>

    <section>
      <h2>Tablica rezultata</h2>
      <div class="table-wrap">{_results_table_html(results)}</div>
    </section>

    <section>
      <h2>Galerija grafikona po metodama</h2>
      <p class="muted">Grafikoni su grupirani po metodi. Graf
      <strong>Rekonstrukcija</strong> najbolje pokazuje utjecaj ispravljanja (original vs degradirano vs rekonstruirano).
      Na dnu su usporedbe koje uključuju sve metode.</p>
      <div class="filters">
        <label>Kategorija
          <select id="filter-category">
            {_filter_options(categories, "Sve kategorije")}
          </select>
        </label>
        <label>Faktor
          <select id="filter-factor">
            {_filter_options([str(f) for f in factors], "Svi faktori")}
          </select>
        </label>
        <label>Metoda
          <select id="filter-method">
            {_filter_options(methods, "Sve metode")}
          </select>
        </label>
        <button type="button" id="reset-filters">Reset</button>
      </div>
      <div id="gallery-by-method">
        {_figure_gallery_sections_html(entries)}
      </div>
    </section>

    <section>
      <h2>Tablice (CSV)</h2>
      <ul class="links">{_table_links_html()}</ul>
    </section>
  </main>

  <script>
    const categorySelect = document.getElementById("filter-category");
    const factorSelect = document.getElementById("filter-factor");
    const methodSelect = document.getElementById("filter-method");
    const resetButton = document.getElementById("reset-filters");
    const cards = Array.from(document.querySelectorAll(".figure-card"));
    const methodSections = Array.from(document.querySelectorAll(".method-section"));

    function applyFilters() {{
      const category = categorySelect.value;
      const factor = factorSelect.value;
      const method = methodSelect.value;

      cards.forEach(card => {{
        const matchCategory = !category || card.dataset.category === category;
        const matchFactor = !factor || card.dataset.factor === factor;
        const matchMethod = !method || card.dataset.method === method;
        card.classList.toggle("hidden", !(matchCategory && matchFactor && matchMethod));
      }});

      methodSections.forEach(section => {{
        const sectionMethod = section.dataset.sectionMethod;
        const visibleCards = section.querySelectorAll(".figure-card:not(.hidden)");
        const matchSectionMethod = !method || !sectionMethod || sectionMethod === method;
        section.classList.toggle(
          "hidden",
          !matchSectionMethod || visibleCards.length === 0
        );
      }});
    }}

    [categorySelect, factorSelect, methodSelect].forEach(el => {{
      el.addEventListener("change", applyFilters);
    }});

    resetButton.addEventListener("click", () => {{
      categorySelect.value = "";
      factorSelect.value = "";
      methodSelect.value = "";
      applyFilters();
    }});
  </script>
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def open_html_report(path: Path | None = None) -> None:
    """Open the HTML report in the default browser."""
    path = path or REPORT_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"HTML report not found: {path}. Run the experiment first."
        )

    resolved = path.resolve()

    # os.startfile handles local paths with Unicode better than file:// URLs on Windows.
    if sys.platform == "win32":
        os.startfile(resolved)
        return

    webbrowser.open(resolved.as_uri())


def report_summary_for_console(path: Path) -> str:
    """Return a short relative path string for terminal output."""
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)
