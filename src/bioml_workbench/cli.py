from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import yaml

from .configuration import AppConfig, load_config
from .pipeline import EndToEndPipeline
from .workflow import TrainingWorkflow


def _format_config(config: AppConfig) -> str:
    return yaml.safe_dump(config.to_dict(), sort_keys=False)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for the BioML Workbench package."""

    parser = argparse.ArgumentParser(
        description="BioML Workbench command-line interface"
    )
    parser.add_argument(
        "--config", type=Path, default=None, help="Path to a YAML config"
    )
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Print the resolved configuration and exit",
    )
    parser.add_argument(
        "--run-workflow",
        action="store_true",
        help="Run a small demo training workflow and save artifacts",
    )
    parser.add_argument(
        "--run-pipeline",
        action="store_true",
        help="Run the end-to-end preprocessing and training pipeline",
    )
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if args.show_config:
        print(_format_config(config))
    elif args.run_workflow:
        workflow = TrainingWorkflow(output_dir="artifacts")
        sample_X = [
            [0.0, 0.0],
            [0.1, 0.0],
            [0.0, 0.1],
            [0.2, 0.1],
            [1.0, 1.0],
            [1.1, 1.0],
            [1.0, 1.1],
            [1.2, 1.1],
        ]
        sample_y = [0, 0, 0, 0, 1, 1, 1, 1]
        result = workflow.run(sample_X, sample_y, model_name="simple_logistic")
        print(f"Workflow completed with accuracy {result['metrics']['accuracy']:.3f}")
    elif args.run_pipeline:
        pipeline = EndToEndPipeline(output_dir="artifacts")
        sample_X = [
            [0.0, 0.0],
            [0.1, 0.0],
            [0.0, 0.1],
            [0.2, 0.1],
            [1.0, 1.0],
            [1.1, 1.0],
            [1.0, 1.1],
            [1.2, 1.1],
        ]
        sample_y = [0, 0, 0, 0, 1, 1, 1, 1]
        result = pipeline.run(sample_X, sample_y, model_name="simple_logistic")
        print(f"Pipeline completed with accuracy {result['metrics']['accuracy']:.3f}")
    else:
        print(f"{config.app_name} is ready.")

    return 0
