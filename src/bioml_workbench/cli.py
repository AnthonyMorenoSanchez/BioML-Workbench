from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .configuration import load_config


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
        print(f"app_name: {config.app_name}")
        print(f"logging.level: {config.logging.level}")
        print(f"logging.to_file: {config.logging.to_file}")
        print(f"logging.file_path: {config.logging.file_path}")
    else:
        print(f"{config.app_name} is ready.")

    return 0
