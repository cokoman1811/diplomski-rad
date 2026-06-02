"""Command-line entry point for thesis experiments."""

import argparse

from .experiment_runner import ExperimentConfig, run_experiments


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Run time-series interpolation experiments for the thesis."
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Use a smaller data slice and fewer degradation factors.",
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run the full experiment grid on the complete dataset.",
    )
    parser.add_argument(
        "--factor",
        type=int,
        action="append",
        dest="factors",
        help="Run only selected degradation factors.",
    )
    parser.add_argument(
        "--method",
        action="append",
        dest="methods",
        help="Run only selected methods.",
    )
    parser.add_argument(
        "--no-tune",
        action="store_true",
        help="Skip ML hyperparameter tuning.",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip figure generation.",
    )
    parser.add_argument(
        "--full-eval",
        action="store_true",
        help="Evaluate on all removed values instead of test period only.",
    )
    parser.add_argument(
        "--open-report",
        action="store_true",
        help="Open the HTML report in the default browser after the run.",
    )
    return parser


def main() -> None:
    """Parse arguments and run experiments."""
    parser = build_parser()
    args = parser.parse_args()

    config = ExperimentConfig(
        quick=args.quick and not args.run_all,
        factors=args.factors or [],
        methods=args.methods or [],
        tune_ml=not args.no_tune,
        use_test_split=not args.full_eval,
        generate_plots=not args.no_plots,
    )

    output = run_experiments(config)

    if args.open_report:
        from .report_html import open_html_report

        open_html_report(output["html_report_path"])


if __name__ == "__main__":
    main()
