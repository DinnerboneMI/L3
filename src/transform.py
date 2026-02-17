from __future__ import annotations

import pandas as pd


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "time" in out.columns:
        out["time"] = pd.to_numeric(out["time"], errors="coerce").astype("Int64")

    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out = out.dropna(subset=["value"])

    if "unit" in out.columns and out["unit"].nunique(dropna=True) > 1:
        most_common = out["unit"].mode(dropna=True).iloc[0]
        out = out[out["unit"] == most_common]

    if "time" in out.columns:
        out = out.dropna(subset=["time"])
        out["time"] = out["time"].astype(int)

    return out
