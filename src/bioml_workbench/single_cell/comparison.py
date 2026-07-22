from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .cohorts import save_cohort_definition, summarize_cohort
from .expression import expression_summary


def export_comparison(
    run_path: str | Path,
    adata: Any,
    cohort_a_definition: dict[str, Any],
    cohort_b_definition: dict[str, Any],
    cohort_a_mask: Any,
    cohort_b_mask: Any,
    genes: list[str],
    layer: str,
    figures: dict[str, Any],
    differential_expression: pd.DataFrame | None = None,
) -> dict[str, str]:
    """Persist reproducible cohort comparison data, figures, and a Markdown report."""
    root = Path(run_path)
    figures_dir = root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    paths["cohort_a"] = str(
        save_cohort_definition(cohort_a_definition, root / "cohort_a.json")
    )
    paths["cohort_b"] = str(
        save_cohort_definition(cohort_b_definition, root / "cohort_b.json")
    )
    summaries = {
        "cohort_a": summarize_cohort(adata, cohort_a_mask, layer),
        "cohort_b": summarize_cohort(adata, cohort_b_mask, layer),
    }
    summary_path = root / "cohort_summary.json"
    summary_path.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    paths["summary"] = str(summary_path)
    for name, mask in {"a": cohort_a_mask, "b": cohort_b_mask}.items():
        path = root / f"selected_cells_{name}.csv"
        pd.DataFrame({"barcode": adata.obs_names[mask].astype(str)}).to_csv(
            path, index=False
        )
        paths[f"selected_cells_{name}"] = str(path)
    summary = expression_summary(
        adata,
        genes,
        {"cohort_a": cohort_a_mask, "cohort_b": cohort_b_mask},
        layer=layer,
    )
    expression_path = root / "gene_expression_summary.csv"
    summary.to_csv(expression_path, index=False)
    paths["expression_summary"] = str(expression_path)
    if differential_expression is not None:
        de_path = root / "differential_expression.csv"
        differential_expression.to_csv(de_path, index=False)
        paths["differential_expression"] = str(de_path)
    figure_paths = []
    for name, figure in figures.items():
        path = figures_dir / f"{name}.html"
        figure.write_html(path)
        figure_paths.append(str(path))
    paths["figures"] = ",".join(figure_paths)
    report = root / "report.md"
    report.write_text(
        "# Cohort Comparison Report\n\n"
        "Single-donor, cell-level comparison. Results are exploratory and not "
        "donor-level inference.\n\n"
        f"- Expression layer: `{layer}`\n"
        f"- Cohort A cells: {summaries['cohort_a']['cell_count']}\n"
        f"- Cohort B cells: {summaries['cohort_b']['cell_count']}\n"
        f"- Selected genes: {', '.join(genes)}\n"
        f"- Figures: {', '.join(figure_paths)}\n",
        encoding="utf-8",
    )
    paths["report"] = str(report)
    return paths
