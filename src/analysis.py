from __future__ import annotations

import pandas as pd


def latest_summary(df: pd.DataFrame) -> tuple[int, pd.DataFrame]:
    latest_year = int(df["time"].max())

    pivot = (
        df[df["time"] == latest_year]
        .pivot_table(index=["geo"], columns=["sex"], values="value", aggfunc="first")
        .reset_index()
    )
    pivot = pivot.rename(columns={"T": "total_%", "M": "men_%", "F": "women_%"}).copy()
    pivot["gender_gap_pp (men-women)"] = pivot["men_%"] - pivot["women_%"]
    return latest_year, pivot


def lt_total_trend(df: pd.DataFrame) -> pd.DataFrame:
    lt = df[(df["geo"] == "LT") & (df["sex"] == "T")][["time", "value"]].sort_values(
        "time"
    )
    lt = lt.rename(columns={"value": "lt_total_%"}).copy()
    lt["yoy_change_pp"] = lt["lt_total_%"].diff()
    return lt


def change_over_period(trend: pd.DataFrame) -> float:
    return float(trend["lt_total_%"].iloc[-1] - trend["lt_total_%"].iloc[0])
