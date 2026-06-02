"""Pretty terminal output for experiments and CLI commands."""

from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path

import pandas as pd
from colorama import Fore, Style, init

from .analysis import best_method_per_factor, build_method_leaderboard
from .config import CLASSICAL_METHODS, ML_METHODS
from .method_info import METHOD_DESCRIPTIONS
from .paths import FIGURES_DIR, PROJECT_ROOT, TABLES_DIR

_BOX_WIDTH = 72


def _stdout_encoding() -> str:
    """Return stdout encoding or utf-8 fallback."""
    return getattr(sys.stdout, "encoding", None) or "utf-8"


def _can_encode(text: str) -> bool:
    """Return True when stdout can print the given text."""
    try:
        text.encode(_stdout_encoding())
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def _glyph(preferred: str, fallback: str) -> str:
    """Pick a glyph supported by the current terminal."""
    return preferred if _can_encode(preferred) else fallback


def _use_color() -> bool:
    """Return True when ANSI colors should be applied."""
    if os.environ.get("NO_COLOR"):
        return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _c(text: str, *styles: str) -> str:
    """Apply color/style when supported."""
    if not _use_color():
        return text
    return "".join(styles) + text + Style.RESET_ALL


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    import re

    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def _visible_len(text: str) -> int:
    """Return printable width ignoring ANSI codes."""
    return len(_strip_ansi(text))


def _pad(text: str, width: int, align: str = "left") -> str:
    """Pad text to a visible column width."""
    padding = max(width - _visible_len(text), 0)
    if align == "right":
        return " " * padding + text
    if align == "center":
        left = padding // 2
        return " " * left + text + " " * (padding - left)
    return text + " " * padding


def _rule(char: str = "─") -> str:
    """Return a horizontal rule."""
    char = _glyph(char, "-")
    return _c(char * _BOX_WIDTH, Fore.BLUE)


def _box_line(text: str, align: str = "center") -> str:
    """Render one line inside a box."""
    inner = _BOX_WIDTH - 4
    content = _pad(text, inner, align=align)
    bar = _glyph("║", "|")
    return _c(f"{bar} ", Fore.CYAN) + content + _c(f" {bar}", Fore.CYAN)


def _configure_stdout() -> None:
    """Use UTF-8 on stdout when the terminal supports it."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def print_banner(title: str, subtitle: str = "") -> None:
    """Print a project banner."""
    _configure_stdout()
    init(autoreset=True)
    top_left = _glyph("╔", "+")
    top_fill = _glyph("═", "=")
    top_right = _glyph("╗", "+")
    bottom_left = _glyph("╚", "+")
    bottom_right = _glyph("╝", "+")

    print()
    print(_c(top_left + top_fill * _BOX_WIDTH + top_right, Fore.CYAN))
    print(_box_line(title))
    if subtitle:
        print(_box_line(subtitle, align="center"))
    print(_c(bottom_left + top_fill * _BOX_WIDTH + bottom_right, Fore.CYAN))
    print()


def print_section(title: str) -> None:
    """Print a section heading."""
    marker = _glyph("▸", ">")
    print(_c(f"{marker} {title}", Fore.YELLOW, Style.BRIGHT))
    print(_rule("─"))


def print_info(message: str) -> None:
    """Print an informational line."""
    bullet = _glyph("•", "-")
    print(_c(f"  {bullet} ", Fore.CYAN) + message)


def print_success(message: str) -> None:
    """Print a success line."""
    mark = _glyph("✓", "OK")
    print(_c(f"  {mark} ", Fore.GREEN, Style.BRIGHT) + message)


def print_warning(message: str) -> None:
    """Print a warning line."""
    mark = _glyph("!", "!")
    print(_c(f"  {mark} ", Fore.YELLOW, Style.BRIGHT) + message)


def print_key_value(label: str, value: str) -> None:
    """Print a label/value pair."""
    print(_c(f"  {label:<18}", Fore.WHITE) + _c(value, Fore.CYAN))


def print_blank() -> None:
    """Print one empty line."""
    print()


def _method_label(method: str) -> str:
    """Return a readable method label."""
    return METHOD_DESCRIPTIONS.get(method, {}).get("name", method)


def print_config_summary(config, dataset_rows: int) -> None:
    """Print experiment configuration summary."""
    mode = "Brzi (--quick)" if config.quick else "Puni (--run-all)"
    tuning = "uključen" if config.tune_ml else "isključen (--no-tune)"
    plots = "da" if config.generate_plots else "ne (--no-plots)"
    eval_scope = (
        "testno razdoblje (2015-2016)" if config.use_test_split else "sve uklonjene tocke"
    )

    classical = [method for method in config.methods if method in CLASSICAL_METHODS]
    ml = [method for method in config.methods if method in ML_METHODS]

    print_section("Konfiguracija")
    print_key_value("Način rada", mode)
    print_key_value("Uzorka podataka", f"{dataset_rows:,}".replace(",", "."))
    print_key_value("Faktori", ", ".join(str(f) for f in config.factors))
    print_key_value("Klasične metode", f"{len(classical)}")
    print_key_value("ML metode", f"{len(ml)}")
    print_key_value("Tuning", tuning)
    print_key_value("Grafikoni", plots)
    print_key_value("Evaluacija", eval_scope)
    print_blank()


def print_progress(
    current: int,
    total: int,
    factor: int,
    method: str,
    metrics: dict[str, float] | None = None,
    width: int = 34,
) -> None:
    """Print an inline progress bar for one experiment step."""
    if total <= 0:
        return

    ratio = current / total
    filled = int(width * ratio)
    fill_char = _glyph("█", "#")
    empty_char = _glyph("░", ".")
    bar = fill_char * filled + empty_char * (width - filled)
    label = _method_label(method)
    status = _c(f"[{bar}]", Fore.GREEN) + f" {current:>2}/{total:<2}  "
    status += _c(f"f={factor}", Fore.MAGENTA) + "  "
    status += _c(f"{label:<18}", Fore.WHITE)

    if metrics:
        status += (
            f"  MAE={metrics['mae']:.4f}  "
            f"RMSE={metrics['rmse']:.4f}  "
            f"R{_glyph('²', '2')}={metrics['r2']:.4f}"
        )

    line = f"\r  {status}"
    print(line, end="", flush=True)
    if current == total:
        print()


def _format_metric(value: float, metric: str) -> str:
    """Format one metric value for display."""
    if metric == "r2":
        return f"{value:7.4f}"
    return f"{value:7.4f}"


def format_results_table(results: pd.DataFrame) -> str:
    """Return a box-drawn results table."""
    if results.empty:
        return "  (nema rezultata)"

    best_by_factor = {
        int(row["factor"]): row["method"]
        for _, row in best_method_per_factor(results).iterrows()
    }

    headers = ["Faktor", "Metoda", "MAE", "RMSE", _glyph("R²", "R2"), "N"]
    rows: list[list[str]] = []
    for _, row in results.sort_values(["factor", "mae"]).iterrows():
        factor = int(row["factor"])
        method = str(row["method"])
        marker = _glyph(" ★", " *") if best_by_factor.get(factor) == method else "  "
        rows.append([
            f"{factor:>6}",
            f"{_method_label(method):<18}{marker}",
            _format_metric(row["mae"], "mae"),
            _format_metric(row["rmse"], "rmse"),
            _format_metric(row["r2"], "r2"),
            f"{int(row['n_samples']):>6}",
        ])

    widths = [
        max(len(headers[index]), max(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]

    def _row(cells: list[str]) -> str:
        parts = [_pad(cell, widths[index]) for index, cell in enumerate(cells)]
        sep = _glyph("│", "|")
        return f"  {sep} " + f" {sep} ".join(parts) + f" {sep}"

    h = _glyph("─", "-")
    v_top = _glyph("┬", "+")
    v_mid = _glyph("┼", "+")
    v_bot = _glyph("┴", "+")
    corner_tl = _glyph("┌", "+")
    corner_tr = _glyph("┐", "+")
    corner_ml = _glyph("├", "+")
    corner_mr = _glyph("┤", "+")
    corner_bl = _glyph("└", "+")
    corner_br = _glyph("┘", "+")
    side = _glyph("│", "|")

    top = f"  {corner_tl}" + v_top.join(h * width for width in widths) + corner_tr
    header = _row(headers)
    sep = f"  {corner_ml}" + v_mid.join(h * width for width in widths) + corner_mr
    bottom = f"  {corner_bl}" + v_bot.join(h * width for width in widths) + corner_br

    body = "\n".join(_row(row) for row in rows)
    star = _glyph("★", "*")
    legend = _c(f"  {star} = najbolja MAE za faktor", Fore.GREEN)
    return "\n".join([top, header, sep, body, bottom, legend])


def print_best_methods(results: pd.DataFrame) -> None:
    """Print best method per degradation factor."""
    best = best_method_per_factor(results)
    print_section("Najbolje metode po faktoru")
    for _, row in best.iterrows():
        line = (
            f"  Faktor {int(row['factor']):>2} {_glyph('->', '->')} "
            f"{_c(_method_label(row['method']), Fore.GREEN, Style.BRIGHT)}  "
            f"(MAE {row['mae']:.4f}, RMSE {row['rmse']:.4f}, "
            f"R{_glyph('²', '2')} {row['r2']:.4f})"
        )
        print(line)
    print_blank()


def print_leaderboard(results: pd.DataFrame, top: int = 5) -> None:
    """Print overall method leaderboard."""
    leaderboard = build_method_leaderboard(results).head(top)
    mean_mae = results.groupby("method")["mae"].mean()

    print_section(f"Leaderboard (top {top})")
    for rank, (_, row) in enumerate(leaderboard.iterrows()):
        medal = {
            0: _glyph("🥇", "1."),
            1: _glyph("🥈", "2."),
            2: _glyph("🥉", "3."),
        }.get(rank, "  ")
        method = row["method"]
        print(
            f"  {medal} {_method_label(method):<18}  "
            f"prosjek ranga: {row['average_rank']:.2f}  "
            f"MAE: {mean_mae[method]:.4f}"
        )
    print_blank()


def _relative_path(path: Path) -> str:
    """Return a project-relative path when possible."""
    try:
        return str(path.relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def print_saved_outputs(
    report_paths: dict | None = None,
    thesis_paths: dict | None = None,
    html_report_path: Path | None = None,
) -> None:
    """Print saved file locations."""
    print_section("Spremljeni rezultati")

    if html_report_path and html_report_path.exists():
        print_success(f"{_relative_path(html_report_path)}  (HTML viewer)")

    core_files = [
        TABLES_DIR / "experiment_results.csv",
        TABLES_DIR / "best_params.json",
    ]
    for path in core_files:
        if path.exists():
            print_success(_relative_path(path))

    if report_paths:
        for path in report_paths.values():
            if isinstance(path, Path) and path.exists():
                print_success(_relative_path(path))

    if thesis_paths:
        for path in thesis_paths.values():
            if isinstance(path, Path) and path.exists():
                print_success(_relative_path(path))

    if FIGURES_DIR.exists():
        figure_count = len(list(FIGURES_DIR.glob("*.png")))
        if figure_count:
            print_info(f"{figure_count} grafikona u {_relative_path(FIGURES_DIR)}/")

    print_blank()


def print_experiment_summary(
    results: pd.DataFrame,
    elapsed_seconds: float,
    report_paths: dict | None = None,
    thesis_paths: dict | None = None,
    html_report_path: Path | None = None,
) -> None:
    """Print the full post-run summary."""
    print_section("Rezultati")
    print(format_results_table(results))
    print_blank()
    print_best_methods(results)
    print_leaderboard(results)
    print_saved_outputs(report_paths, thesis_paths, html_report_path)

    if html_report_path and html_report_path.exists():
        print_info(f"Otvori izvjestaj: start results\\report.html")
        print_info(f"ili pokreni: open_report.bat")

    minutes, seconds = divmod(elapsed_seconds, 60)
    if minutes >= 1:
        duration = f"{int(minutes)} min {seconds:.1f} s"
    else:
        duration = f"{seconds:.1f} s"

    print(_rule(_glyph("═", "=")))
    done = _glyph("✓", "OK")
    print(_c(f"  {done} Eksperiment uspješno završen za {duration}", Fore.GREEN, Style.BRIGHT))
    print(_rule(_glyph("═", "=")))
    print()


def print_download_start(url: str) -> None:
    """Print dataset download start message."""
    print_section("Preuzimanje podataka")
    print_info("Jena Climate dataset")
    print_key_value("URL", textwrap.shorten(url, width=52, placeholder="…"))


def print_download_complete(path: Path) -> None:
    """Print dataset download completion message."""
    print_success(f"Datoteka spremljena: {_relative_path(path)}")


def print_data_ready(path: Path) -> None:
    """Print message when local data is already available."""
    print_success(f"Podaci su spremni: {_relative_path(path)}")


def print_quality_report(report: dict) -> None:
    """Print a formatted data quality report."""
    print_banner("Provjera podataka", "Jena Climate dataset")

    sampling = report.get("sampling", {})
    print_section("Uzorkovanje")
    print_key_value("Broj redaka", f"{sampling.get('n_rows', 0):,}".replace(",", "."))
    print_key_value("Veliki gapovi", str(sampling.get("large_gaps", 0)))
    print_key_value("Duplikati", str(sampling.get("duplicate_timestamps", 0)))
    print_key_value(
        "Pokrivenost po satu",
        f"{report.get('hourly_coverage_min', 0)} – {report.get('hourly_coverage_max', 0)}",
    )

    temperature = report.get("temperature", {})
    if temperature:
        print_blank()
        print_section("Temperatura")
        print_key_value("Min", f"{temperature.get('min', 0):.2f} C")
        print_key_value("Max", f"{temperature.get('max', 0):.2f} C")
        print_key_value("Prosjek", f"{temperature.get('mean', 0):.2f} C")
        print_key_value("Std", f"{temperature.get('std', 0):.2f}")
        print_key_value("Missing", f"{temperature.get('missing_pct', 0):.2f} %")

    covariates = report.get("covariates", [])
    if covariates:
        print_blank()
        print_section("Covariates")
        for row in covariates:
            print_info(
                f"{row['column']}: {row['min']:.1f} – {row['max']:.1f} "
                f"(missing {row['missing_pct']:.2f} %)"
            )

    print_blank()


def print_benchmark_table(table_text: str) -> None:
    """Print a benchmark table with a header."""
    print_banner("Benchmark metoda", "Vrijeme izvršavanja")
    print_section("Rezultati")
    for line in table_text.splitlines():
        print(f"  {line}")
    print_blank()


def print_method_catalog(text: str) -> None:
    """Print method catalog markdown with spacing."""
    print_banner("Katalog metoda", "Klasične i ML metode")
    print(text)
    print_blank()
