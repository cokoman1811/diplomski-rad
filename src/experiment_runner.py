"""Run interpolation and ML experiments."""

import time
from dataclasses import dataclass, field

import pandas as pd

from .console import (
    print_banner,
    print_config_summary,
    print_experiment_summary,
    print_progress,
    print_section,
)

from .config import (
    ALL_METHODS,
    CLASSICAL_METHODS,
    DEGRADATION_FACTORS,
    ML_METHODS,
    QUICK_DEGRADATION_FACTORS,
    QUICK_SAMPLE_SIZE,
    TEST_START,
)
from .data_loader import load_jena_dataset
from .evaluation import aggregate_results, compute_metrics, compute_point_errors
from .feature_engineering import (
    build_feature_matrix,
    build_train_test_masks,
    get_prediction_rows,
    get_training_rows,
)
from .interpolation_methods import interpolate
from .io_utils import save_json, save_results_table
from .ml_models import reconstruct_with_ml
from .paths import PROJECT_ROOT, ensure_project_dirs
from .plots import (
    plot_all_factor_rankings,
    plot_all_metric_lines,
    plot_error_boxplot,
    plot_error_by_hour,
    plot_error_by_month,
    plot_error_histogram,
    plot_metric_bars,
    plot_metric_heatmap,
    plot_reconstruction_window,
    plot_residual_scatter,
)
from .preprocessing import DegradedSeries, degrade_series, evaluation_mask
from .reporting import save_all_reports, update_results_notes_template
from .statistical_analysis import (
    build_error_matrix,
    compare_methods_for_factor,
    friedman_test,
    summarize_errors,
)


@dataclass
class ExperimentConfig:
    """Configuration for a single experiment run."""

    quick: bool = False
    factors: list[int] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    tune_ml: bool = True
    use_test_split: bool = True
    generate_plots: bool = True

    def __post_init__(self) -> None:
        if not self.factors:
            self.factors = QUICK_DEGRADATION_FACTORS if self.quick else DEGRADATION_FACTORS
        if not self.methods:
            self.methods = list(ALL_METHODS)


def _prepare_dataset(config: ExperimentConfig) -> pd.DataFrame:
    """Load dataset and optionally slice for quick mode."""
    dataset = load_jena_dataset()
    if config.quick:
        split = pd.Timestamp(TEST_START)
        split_idx = dataset.index.searchsorted(split)
        half = QUICK_SAMPLE_SIZE // 2
        start = max(0, split_idx - half)
        end = min(len(dataset), start + QUICK_SAMPLE_SIZE)
        start = max(0, end - QUICK_SAMPLE_SIZE)
        dataset = dataset.iloc[start:end]
    return dataset


def _reconstruct_classical(degraded: pd.Series, method: str) -> pd.Series:
    """Apply a classical interpolation method."""
    return interpolate(degraded, method)


def _reconstruct_ml(
    dataset: pd.DataFrame,
    degraded: DegradedSeries,
    method: str,
    train_mask: pd.Series,
    config: ExperimentConfig,
    cached_params: dict,
) -> pd.Series:
    """Apply an ML reconstruction method."""
    features = build_feature_matrix(dataset, degraded.degraded)
    train_rows = get_training_rows(degraded.degraded, train_mask)
    predict_rows = get_prediction_rows(degraded.degraded)

    params = cached_params.get(method)
    reconstructed, used_params = reconstruct_with_ml(
        method=method,
        features=features,
        degraded=degraded.degraded,
        train_rows=train_rows,
        predict_rows=predict_rows,
        params=params,
        tune=config.tune_ml and params is None,
    )
    if method not in cached_params:
        cached_params[method] = used_params
    return reconstructed


def run_single_method(
    dataset: pd.DataFrame,
    degraded: DegradedSeries,
    method: str,
    train_mask: pd.Series,
    test_mask: pd.Series,
    config: ExperimentConfig,
    cached_params: dict,
) -> tuple[pd.Series, dict, pd.Series]:
    """Run one method and return reconstruction, metrics and errors."""
    if method in CLASSICAL_METHODS:
        reconstructed = _reconstruct_classical(degraded.degraded, method)
    elif method in ML_METHODS:
        reconstructed = _reconstruct_ml(
            dataset, degraded, method, train_mask, config, cached_params
        )
    else:
        raise ValueError(f"Unknown method: {method}")

    eval_mask = evaluation_mask(
        degraded.removed_mask,
        test_mask if config.use_test_split else None,
    )
    metrics = compute_metrics(degraded.original, reconstructed, eval_mask)
    errors = compute_point_errors(degraded.original, reconstructed, eval_mask)

    if config.generate_plots and method in {"linear", "random_forest", "cubic"}:
        plot_residual_scatter(degraded.original, reconstructed, eval_mask, method, degraded.factor)
        plot_error_histogram(errors, method, degraded.factor)

    return reconstructed, metrics, errors


def run_experiments(config: ExperimentConfig | None = None) -> dict:
    """Run the full experiment grid and save outputs."""
    config = config or ExperimentConfig()
    ensure_project_dirs()
    started_at = time.perf_counter()

    dataset = _prepare_dataset(config)
    temperature = dataset["temperature"]
    train_mask, test_mask = build_train_test_masks(temperature.index)

    print_banner(
        "Interpolacija vremenskih serija",
        "Diplomski rad · Jena Climate · temperatura",
    )
    print_config_summary(config, len(dataset))

    total_runs = len(config.factors) * len(config.methods)
    run_index = 0

    results = []
    best_params = {}
    error_by_factor = {}
    summary_by_factor = {}

    print_section("Pokretanje eksperimenta")

    for factor in config.factors:
        degraded = degrade_series(temperature, factor)
        method_errors = {}

        for method in config.methods:
            run_index += 1

            reconstructed, metrics, errors = run_single_method(
                dataset,
                degraded,
                method,
                train_mask,
                test_mask,
                config,
                best_params,
            )

            if method in ML_METHODS and method not in best_params:
                best_params[method] = best_params.get(method, {})

            method_errors[method] = errors
            results.append({
                "factor": factor,
                "method": method,
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "r2": metrics["r2"],
                "n_samples": metrics["n_samples"],
            })

            print_progress(
                run_index,
                total_runs,
                factor,
                method,
                metrics,
            )

            if config.generate_plots and method in {"linear", "random_forest"}:
                plot_reconstruction_window(
                    degraded.original,
                    degraded.degraded,
                    reconstructed,
                    method,
                    factor,
                )
                plot_error_by_hour(errors, method, factor)
                plot_error_by_month(errors, method, factor)

        error_frame = build_error_matrix(method_errors)
        error_by_factor[factor] = error_frame
        summary_by_factor[factor] = {
            method: summarize_errors(errors)
            for method, errors in method_errors.items()
        }

        if config.generate_plots:
            plot_error_boxplot(error_frame, factor)

        friedman = friedman_test(error_frame)
        save_json(friedman, f"friedman_factor_{factor}.json")
        comparison = compare_methods_for_factor(method_errors, baseline_method="linear")
        save_results_table(comparison, f"wilcoxon_vs_linear_factor_{factor}.csv")

    results_df = aggregate_results(results)
    save_results_table(results_df, "experiment_results.csv")
    save_json(best_params, "best_params.json")

    if config.generate_plots:
        for metric in ("mae", "rmse", "r2"):
            plot_metric_bars(results_df, metric)
            plot_metric_heatmap(results_df, metric)

    save_json(summary_by_factor, "error_summary_by_factor.json")

    report_paths = save_all_reports(results_df, summary_by_factor, best_params)
    notes_path = PROJECT_ROOT / "docs" / "results_notes.md"
    update_results_notes_template(results_df, notes_path)

    from .thesis_export import export_all_thesis_tables

    thesis_paths = export_all_thesis_tables(results_df)

    if config.generate_plots:
        plot_all_factor_rankings(results_df)
        plot_all_metric_lines(results_df)

    from .report_html import generate_html_report

    html_report_path = generate_html_report(results_df)

    elapsed = time.perf_counter() - started_at
    print_experiment_summary(
        results_df,
        elapsed,
        report_paths=report_paths,
        thesis_paths=thesis_paths,
        html_report_path=html_report_path,
    )

    return {
        "results": results_df,
        "best_params": best_params,
        "error_by_factor": error_by_factor,
        "summary_by_factor": summary_by_factor,
        "report_paths": report_paths,
        "thesis_paths": thesis_paths,
        "html_report_path": html_report_path,
        "elapsed_seconds": elapsed,
    }
