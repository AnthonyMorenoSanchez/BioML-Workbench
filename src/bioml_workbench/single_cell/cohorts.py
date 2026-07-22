from __future__ import annotations

import json
from difflib import get_close_matches
from pathlib import Path
from typing import Any, cast

import numpy as np
from scipy.sparse import issparse  # type: ignore[import-untyped]


def create_cohort_definition(
    name: str,
    filters: list[dict[str, Any]],
    description: str = "",
    expression_layer: str = "X",
    logic: str = "AND",
) -> dict[str, Any]:
    """Create a serializable cohort rule definition."""
    if not name.strip():
        raise ValueError("Cohort name cannot be empty")
    if logic not in {"AND", "OR"}:
        raise ValueError("Cohort logic must be AND or OR")
    return {
        "name": name,
        "description": description,
        "expression_layer": expression_layer,
        "filters": filters,
        "logic": logic,
    }


def validate_cohort(adata: Any, definition: dict[str, Any]) -> dict[str, Any]:
    """Validate declared layers, filters, genes, columns, and barcode lists."""
    errors: list[str] = []
    layer = definition.get("expression_layer", "X")
    if layer != "X" and layer not in adata.layers:
        errors.append(f"Unknown expression layer: {layer}")
    for item in definition.get("filters", []):
        filter_type = item.get("type")
        if filter_type in {"metadata", "qc"} and item.get("column") not in adata.obs:
            errors.append(f"Unknown metadata column: {item.get('column')}")
        if filter_type == "gene" and item.get("gene") not in adata.var_names:
            suggestions = get_close_matches(str(item.get("gene")), adata.var_names, n=3)
            suffix = f"; did you mean {', '.join(suggestions)}?" if suggestions else ""
            errors.append(f"Unknown gene: {item.get('gene')}{suffix}")
        if filter_type == "barcode":
            values = item.get("values", [])
            if len(values) != len(set(values)):
                errors.append("Barcode filter contains duplicate barcodes")
        if filter_type not in {"metadata", "qc", "gene", "barcode"}:
            errors.append(f"Unsupported filter type: {filter_type}")
    return {"valid": not errors, "errors": errors, "layer": layer}


def _matrix_for_layer(adata: Any, layer: str) -> Any:
    return adata.X if layer == "X" else adata.layers[layer]


def _gene_values(adata: Any, gene: str, layer: str) -> np.ndarray:
    index = adata.var_names.get_loc(gene)
    values = _matrix_for_layer(adata, layer)[:, index]
    if issparse(values):
        return np.asarray(values.toarray()).ravel()
    return np.asarray(values).ravel()


def _numeric_match(
    values: np.ndarray, operator: str, value: float, maximum: Any
) -> np.ndarray:
    if operator == ">":
        return values > value
    if operator == ">=":
        return values >= value
    if operator == "<":
        return values < value
    if operator == "<=":
        return values <= value
    if operator == "between":
        if maximum is None:
            raise ValueError("between filters require a maximum value")
        return (values >= value) & (values <= float(maximum))
    raise ValueError(f"Unsupported numeric operator: {operator}")


def resolve_cohort(
    adata: Any, definition: dict[str, Any]
) -> tuple[np.ndarray, dict[str, Any]]:
    """Resolve a rule definition into an obs-aligned boolean mask and report."""
    validation = validate_cohort(adata, definition)
    if not validation["valid"]:
        raise ValueError("; ".join(validation["errors"]))
    layer = validation["layer"]
    filters = definition.get("filters", [])
    masks: list[np.ndarray] = []
    for item in filters:
        operator = item.get("operator")
        filter_type = item["type"]
        if filter_type in {"metadata", "qc"}:
            values = adata.obs[item["column"]].to_numpy()
            if operator == "in":
                masks.append(
                    np.isin(values.astype(str), [str(v) for v in item["values"]])
                )
            elif operator == "not_in":
                masks.append(
                    ~np.isin(values.astype(str), [str(v) for v in item["values"]])
                )
            else:
                masks.append(
                    _numeric_match(
                        values.astype(float),
                        operator,
                        float(item["value"]),
                        item.get("max"),
                    )
                )
        elif filter_type == "barcode":
            values = np.asarray([str(value) for value in adata.obs_names])
            included = np.isin(values, [str(v) for v in item["values"]])
            masks.append(~included if operator == "not_in" else included)
        else:
            masks.append(
                _numeric_match(
                    _gene_values(adata, item["gene"], layer),
                    operator,
                    float(item["value"]),
                    item.get("max"),
                )
            )
    if not masks:
        mask = np.ones(adata.n_obs, dtype=bool)
    elif definition.get("logic", "AND") == "OR":
        mask = np.logical_or.reduce(masks)
    else:
        mask = np.logical_and.reduce(masks)
    report = {
        "name": definition["name"],
        "cell_count": int(mask.sum()),
        "layer": layer,
        "validation": validation,
    }
    if not mask.any():
        report["warning"] = "Cohort is empty"
    return mask, report


def summarize_cohort(adata: Any, mask: np.ndarray, layer: str = "X") -> dict[str, Any]:
    """Summarize a cohort without copying its full expression matrix."""
    if len(mask) != adata.n_obs:
        raise ValueError("Cohort mask must align with adata.obs_names")
    return {
        "cell_count": int(mask.sum()),
        "layer": layer,
        "barcodes": [str(item) for item in adata.obs_names[mask]],
    }


def save_cohort_definition(definition: dict[str, Any], path: str | Path) -> Path:
    """Persist a cohort rule definition as JSON."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(definition, indent=2), encoding="utf-8")
    return output


def load_cohort_definition(path: str | Path) -> dict[str, Any]:
    """Load a persisted cohort rule definition."""
    return cast(dict[str, Any], json.loads(Path(path).read_text(encoding="utf-8")))
