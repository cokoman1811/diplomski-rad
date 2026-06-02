"""Generate markdown and CSV reports from experiment outputs."""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from .analysis import (
    best_method_per_factor,
    build_method_leaderboard,
    classical_ml_gap,
    compare_classical_vs_ml,
    method_stability_score,
    rank_methods_by_metric,
)
from .config import ALL_METHODS, DEGRADATION_FACTORS, ML_METHODS
from .io_utils import save_results_table
from .paths import PROJECT_ROOT, TABLES_DIR, ensure_project_dirs


def _dataframe_to_markdown(frame: pd.DataFrame) -> str:
    """Convert a DataFrame to a simple markdown table without extra dependencies."""
    columns = list(frame.columns)
    header = "| " + " | ".join(str(col) for col in columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for row in frame.itertuples(index=False):
        rows.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join([header, separator, *rows])


def _format_results_table(results: pd.DataFrame) -> str:
    """Format main results as a markdown table."""
    display = results.copy()
    for column in ("mae", "rmse", "r2"):
        if column in display.columns:
            display[column] = display[column].map(lambda x: f"{x:.4f}")
    return _dataframe_to_markdown(display)


def _format_leaderboard(leaderboard: pd.DataFrame) -> str:
    """Format leaderboard as markdown."""
    frame = leaderboard.copy()
    frame["average_rank"] = frame["average_rank"].map(lambda x: f"{x:.2f}")
    return _dataframe_to_markdown(frame)


def generate_results_markdown(
    results: pd.DataFrame,
    summary_by_factor: dict | None = None,
    best_params: dict | None = None,
) -> str:
    """Build a markdown report string from experiment outputs."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ranked = rank_methods_by_metric(results)
    best = best_method_per_factor(results)
    leaderboard = build_method_leaderboard(results)
    stability = method_stability_score(results)
    classical_vs_ml = compare_classical_vs_ml(results)
    gap = classical_ml_gap(results)

    lines = [
        "# Experiment report",
        "",
        f"Generated: {timestamp}",
        "",
        "## Setup",
        "",
        f"- Methods: {', '.join(ALL_METHODS)}",
        f"- Degradation factors: {', '.join(str(f) for f in sorted(results['factor'].unique()))}",
        f"- Evaluation metrics: MAE, RMSE, R²",
        "",
        "## Main results",
        "",
        _format_results_table(results),
        "",
        "## Best method per factor",
        "",
        _dataframe_to_markdown(best),
        "",
        "## Method leaderboard (average rank by MAE)",
        "",
        _format_leaderboard(leaderboard),
        "",
        "## Stability across factors",
        "",
        _dataframe_to_markdown(stability),
        "",
        "## Classical vs ML summary",
        "",
        _dataframe_to_markdown(classical_vs_ml),
        "",
        "## Best ML vs best classical gap",
        "",
        _dataframe_to_markdown(gap) if not gap.empty else "_No ML/classical comparison available._",
        "",
    ]

    if best_params:
        lines.extend([
            "## ML hyperparameters",
            "",
            "```json",
            json.dumps(best_params, indent=2),
            "```",
            "",
        ])

    if summary_by_factor:
        lines.extend(["## Error summaries by factor", ""])
        for factor, summaries in summary_by_factor.items():
            lines.append(f"### Factor {factor}")
            lines.append("")
            summary_df = pd.DataFrame(summaries).T
            lines.append(_dataframe_to_markdown(summary_df))
            lines.append("")

    lines.extend([
        "## Notes for thesis writing",
        "",
        "- Rezultati pokazuju kako se pogreška povećava s faktorom degradacije.",
        "- Usporedba klasičnih metoda i ML modela treba interpretirati uzimajući u obzir tuning.",
        "- Detaljne statističke usporedbe nalaze se u `wilcoxon_vs_linear_factor_*.csv`.",
        "",
    ])
    return "\n".join(lines)


def save_results_report(
    results: pd.DataFrame,
    summary_by_factor: dict | None = None,
    best_params: dict | None = None,
    filename: str = "experiment_report.md",
) -> Path:
    """Save markdown report to results/tables/."""
    ensure_project_dirs()
    content = generate_results_markdown(results, summary_by_factor, best_params)
    path = TABLES_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path


def save_ranked_results(results: pd.DataFrame) -> Path:
    """Save ranked results table."""
    ranked = rank_methods_by_metric(results)
    return save_results_table(ranked, "experiment_results_ranked.csv")


def save_best_methods_table(results: pd.DataFrame) -> Path:
    """Save best method per factor table."""
    best = best_method_per_factor(results)
    return save_results_table(best, "best_method_per_factor.csv")


def save_leaderboard(results: pd.DataFrame) -> Path:
    """Save overall method leaderboard."""
    leaderboard = build_method_leaderboard(results)
    return save_results_table(leaderboard, "method_leaderboard.csv")


def save_classical_ml_comparison(results: pd.DataFrame) -> Path:
    """Save classical vs ML comparison table."""
    comparison = compare_classical_vs_ml(results)
    return save_results_table(comparison, "classical_vs_ml_summary.csv")


def save_all_reports(
    results: pd.DataFrame,
    summary_by_factor: dict | None = None,
    best_params: dict | None = None,
) -> dict[str, Path]:
    """Save all derived report artifacts."""
    paths = {
        "markdown": save_results_report(results, summary_by_factor, best_params),
        "ranked": save_ranked_results(results),
        "best_methods": save_best_methods_table(results),
        "leaderboard": save_leaderboard(results),
        "classical_vs_ml": save_classical_ml_comparison(results),
    }
    stability = method_stability_score(results)
    paths["stability"] = save_results_table(stability, "method_stability.csv")
    gap = classical_ml_gap(results)
    if not gap.empty:
        paths["gap"] = save_results_table(gap, "classical_ml_gap.csv")
    return paths


def update_results_notes_template(results: pd.DataFrame, docs_path: Path) -> Path:
    """Append a short auto-generated summary block to docs/results_notes.md."""
    best = best_method_per_factor(results)
    leaderboard = build_method_leaderboard(results).head(3)
    block = [
        "",
        "---",
        "",
        "## Auto-generated summary",
        "",
        f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "### Top methods overall",
        "",
        _format_leaderboard(leaderboard),
        "",
        "### Best method per factor",
        "",
        _dataframe_to_markdown(best),
        "",
    ]
    existing = docs_path.read_text(encoding="utf-8") if docs_path.exists() else ""
    marker = "## Auto-generated summary"
    if marker in existing:
        existing = existing.split(marker)[0].rstrip()
    docs_path.write_text(existing + "\n".join(block), encoding="utf-8")
    return docs_path
