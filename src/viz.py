from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_lt_vs_eu_total(
    df: pd.DataFrame,
    out_path: Path,
    target_2030: float,
) -> None:
    plot_df = df[(df["geo"].isin(["LT", "EU27_2020"])) & (df["sex"] == "T")].copy()

    label_map = {"LT": "Lithuania", "EU27_2020": "EU27"}

    plt.figure()
    for g in ["LT", "EU27_2020"]:
        part = plot_df[plot_df["geo"] == g].sort_values("time")
        plt.plot(part["time"], part["value"], label=label_map[g])

    plt.axhline(target_2030, linestyle="--", linewidth=1, label="Target (9%)")
    plt.title("Early leavers (18–24), Total (%) — Lithuania vs EU27")
    plt.xlabel("Year")
    plt.ylabel("% of population 18–24")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)

def plot_lt_absolute_count(
    df_abs: pd.DataFrame,
    out_path: Path,
) -> None:
    plt.figure()
    part = df_abs.sort_values("time")
    plt.plot(part["time"], part["early_leavers_count"], label="Lithuania (absolute)")

    plt.title("Early leavers (18–24), Lithuania — absolute count (estimated)")
    plt.xlabel("Year")
    plt.ylabel("People (18–24)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
