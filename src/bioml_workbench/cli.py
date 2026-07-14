from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import yaml

from .configuration import AppConfig, load_config


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
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if args.show_config:
        print(_format_config(config))
    else:
        print(f"{config.app_name} is ready.")

    return 0
