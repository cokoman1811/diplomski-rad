"""Export helpers for thesis tables and discussion text."""

from pathlib import Path

import pandas as pd

from .analysis import (
    best_method_per_factor,
    build_method_leaderboard,
    classical_ml_gap,
    compare_classical_vs_ml,
    method_stability_score,
    pivot_results,
    rank_methods_by_metric,
)
from .config import CLASSICAL_METHODS, DEGRADATION_FACTORS, ML_METHODS
from .io_utils import save_results_table
from .method_info import full_method_catalog_markdown, get_method_description
from .paths import TABLES_DIR, ensure_project_dirs


def export_metric_pivot_tables(results: pd.DataFrame) -> dict[str, Path]:
    """Export MAE, RMSE and R2 pivot tables."""
    ensure_project_dirs()
    paths = {}
    for metric in ("mae", "rmse", "r2"):
        pivot = pivot_results(results, metric)
        filename = f"pivot_{metric}.csv"
        paths[metric] = save_results_table(pivot.reset_index(), filename)
    return paths


def export_ranked_results(results: pd.DataFrame) -> Path:
    """Export ranked results table."""
    ranked = rank_methods_by_metric(results)
    return save_results_table(ranked, "thesis_ranked_results.csv")


def export_best_methods(results: pd.DataFrame) -> Path:
    """Export best method per factor table."""
    return save_results_table(best_method_per_factor(results), "thesis_best_methods.csv")


def export_leaderboard(results: pd.DataFrame) -> Path:
    """Export overall leaderboard."""
    return save_results_table(build_method_leaderboard(results), "thesis_leaderboard.csv")


def export_stability(results: pd.DataFrame) -> Path:
    """Export stability scores."""
    return save_results_table(method_stability_score(results), "thesis_method_stability.csv")


def export_classical_ml_summary(results: pd.DataFrame) -> Path:
    """Export classical vs ML summary."""
    return save_results_table(compare_classical_vs_ml(results), "thesis_classical_vs_ml.csv")


def export_classical_ml_gap(results: pd.DataFrame) -> Path:
    """Export gap between best classical and best ML."""
    gap = classical_ml_gap(results)
    return save_results_table(gap, "thesis_classical_ml_gap.csv")


def build_croatian_summary_sentences(results: pd.DataFrame) -> list[str]:
    """Generate Croatian thesis sentences from results."""
    best = best_method_per_factor(results)
    leaderboard = build_method_leaderboard(results)
    top_method = leaderboard.iloc[0]["method"]
    sentences = [
        "Rezultati pokazuju razlike u točnosti rekonstrukcije ovisno o metodi i faktoru degradacije.",
        f"Najbolja metoda prema prosječnom rangu je {top_method}.",
    ]
    for _, row in best.iterrows():
        sentences.append(
            f"Za faktor degradacije {int(row['factor'])} najbolju MAE postiže metoda {row['method']} "
            f"(MAE = {row['mae']:.4f})."
        )
    return sentences


def build_english_summary_sentences(results: pd.DataFrame) -> list[str]:
    """Generate English thesis sentences from results."""
    best = best_method_per_factor(results)
    sentences = [
        "The results show that reconstruction accuracy depends on both the method and degradation factor.",
    ]
    for _, row in best.iterrows():
        sentences.append(
            f"For degradation factor {int(row['factor'])}, the best MAE is achieved by {row['method']} "
            f"(MAE = {row['mae']:.4f})."
        )
    return sentences


def export_summary_sentences(results: pd.DataFrame) -> Path:
    """Save Croatian and English summary sentences to a text file."""
    ensure_project_dirs()
    lines = ["# Thesis summary sentences", ""]
    lines.append("## Croatian")
    lines.extend(build_croatian_summary_sentences(results))
    lines.append("")
    lines.append("## English")
    lines.extend(build_english_summary_sentences(results))
    path = TABLES_DIR / "thesis_summary_sentences.txt"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def export_method_catalog() -> Path:
    """Export method catalog markdown for thesis appendix."""
    ensure_project_dirs()
    path = TABLES_DIR / "thesis_method_catalog.md"
    path.write_text(full_method_catalog_markdown(), encoding="utf-8")
    return path


def export_method_metadata_table() -> Path:
    """Export method metadata as CSV."""
    rows = []
    for method in CLASSICAL_METHODS + ML_METHODS:
        info = get_method_description(method)
        rows.append({
            "method": method,
            "name": info["name"],
            "category": info["category"],
            "uses_covariates": info["uses_covariates"],
            "needs_training": info["needs_training"],
        })
    return save_results_table(pd.DataFrame(rows), "thesis_method_metadata.csv")


def export_factor_definitions() -> Path:
    """Export degradation factor definitions."""
    rows = []
    for factor in DEGRADATION_FACTORS:
        rows.append({
            "factor": factor,
            "original_resolution_minutes": 10,
            "simulated_resolution_minutes": 10 * factor,
        })
    return save_results_table(pd.DataFrame(rows), "thesis_factor_definitions.csv")


def export_all_thesis_tables(results: pd.DataFrame) -> dict[str, Path]:
    """Export all thesis helper tables and text files."""
    paths = {}
    paths.update(export_metric_pivot_tables(results))
    paths["ranked"] = export_ranked_results(results)
    paths["best_methods"] = export_best_methods(results)
    paths["leaderboard"] = export_leaderboard(results)
    paths["stability"] = export_stability(results)
    paths["classical_vs_ml"] = export_classical_ml_summary(results)
    gap = classical_ml_gap(results)
    if not gap.empty:
        paths["gap"] = export_classical_ml_gap(results)
    paths["summary_sentences"] = export_summary_sentences(results)
    paths["method_catalog"] = export_method_catalog()
    paths["method_metadata"] = export_method_metadata_table()
    paths["factor_definitions"] = export_factor_definitions()
    return paths
