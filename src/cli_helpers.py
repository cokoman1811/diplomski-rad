"""CLI helper utilities."""

import argparse
from pathlib import Path

from .benchmarks import benchmark_methods, format_benchmark_table
from .console import (
    print_banner,
    print_benchmark_table,
    print_method_catalog,
    print_quality_report,
    print_section,
    print_success,
)
from .data_quality import full_quality_report
from .data_loader import load_jena_dataset
from .download_data import ensure_jena_data
from .experiment_runner import ExperimentConfig, run_experiments
from .method_info import full_method_catalog_markdown
from .preprocessing import slice_dataset_recent
from .thesis_export import export_all_thesis_tables
from .validation import validate_dataset_frame


def build_extended_parser() -> argparse.ArgumentParser:
    """Build parser with subcommands for common thesis tasks."""
    parser = argparse.ArgumentParser(description="Thesis project helper commands")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("check-data", help="Validate Jena dataset quality")
    subparsers.add_parser("download-data", help="Download Jena dataset if missing")
    subparsers.add_parser("method-catalog", help="Print method catalog markdown")

    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark method runtime")
    benchmark_parser.add_argument("--sample-size", type=int, default=5000)

    export_parser = subparsers.add_parser("export-thesis", help="Run quick experiment and export thesis tables")
    export_parser.add_argument("--quick", action="store_true")

    return parser


def run_check_data() -> dict:
    """Load data and print quality report."""
    ensure_jena_data()
    dataset = load_jena_dataset()
    validate_dataset_frame(dataset)
    return full_quality_report(dataset)


def run_download_data() -> Path:
    """Download Jena dataset."""
    return ensure_jena_data()


def run_method_catalog() -> str:
    """Return method catalog markdown."""
    return full_method_catalog_markdown()


def run_benchmark(sample_size: int = 5000) -> str:
    """Benchmark all methods and return formatted table."""
    frame = benchmark_methods(sample_size=sample_size)
    return format_benchmark_table(frame)


def run_export_thesis(quick: bool = True) -> dict:
    """Run experiment and export thesis tables."""
    config = ExperimentConfig(
        quick=quick,
        tune_ml=not quick,
        generate_plots=True,
    )
    output = run_experiments(config)
    paths = export_all_thesis_tables(output["results"])
    return {"results": output["results"], "paths": paths}


def dispatch_cli(args: argparse.Namespace) -> object:
    """Dispatch CLI subcommand."""
    if args.command == "check-data":
        report = run_check_data()
        print_quality_report(report)
        return report
    if args.command == "download-data":
        path = run_download_data()
        print_banner("Preuzimanje podataka", "Jena Climate dataset")
        print_success(f"Podaci spremni: {path}")
        return path
    if args.command == "method-catalog":
        text = run_method_catalog()
        print_method_catalog(text)
        return text
    if args.command == "benchmark":
        text = run_benchmark(args.sample_size)
        print_benchmark_table(text)
        return text
    if args.command == "export-thesis":
        output = run_export_thesis(args.quick)
        print_section("Izvoz tablica za tezu")
        for path in output["paths"].values():
            print_success(str(path))
        return output
    raise ValueError(f"Unknown command: {args.command}")
