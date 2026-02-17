from __future__ import annotations

import itertools
from typing import Any, Dict, List, Sequence

import pandas as pd


def _dimension_ids(js: Dict[str, Any]) -> Sequence[str]:
    if "id" in js and isinstance(js["id"], list):
        return js["id"]
    dim = js.get("dimension", {})
    if "id" in dim and isinstance(dim["id"], list):
        return dim["id"]
    # fallback: take keys except service keys
    return [k for k in dim.keys() if k not in ("id", "size")]


def jsonstat_to_df(js: Dict[str, Any]) -> pd.DataFrame:
    dim = js["dimension"]
    dim_ids = list(_dimension_ids(js))

    dim_values: List[List[str]] = []
    for d in dim_ids:
        cat = dim[d]["category"]
        idx = cat.get("index")

        if isinstance(idx, dict):
            codes = sorted(idx, key=idx.get)
        elif isinstance(idx, list):
            codes = idx
        else:
            codes = list(cat["label"].keys())

        dim_values.append(list(codes))

    rows = list(itertools.product(*dim_values))
    df = pd.DataFrame(rows, columns=dim_ids)

    vals = js.get("value")
    if isinstance(vals, dict):
        full = [None] * len(rows)
        for k, v in vals.items():
            full[int(k)] = v
        vals = full

    df["value"] = vals
    return df
