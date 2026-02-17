from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analysis import change_over_period, latest_summary, lt_total_trend
from src.config import Settings
from src.eurostat_client import fetch_jsonstat
from src.jsonstat import jsonstat_to_df
from src.transform import clean_df
from src.viz import plot_lt_vs_eu_total


def build_params(settings: Settings) -> list[tuple[str, str]]:
    params: list[tuple[str, str]] = [("format", "JSON"), ("lang", "EN")]
    params += [("geo", g) for g in settings.geos]
    params += [("sex", s) for s in settings.sexes]
    params += [("time", str(y)) for y in settings.years]
    return params


def main() -> None:
    settings = Settings()
    outdir = Path("output")
    outdir.mkdir(exist_ok=True)

    params = build_params(settings)
    js = fetch_jsonstat(settings.endpoint, params)

    df = jsonstat_to_df(js)
    df = df.dropna(subset=["value"])
    df = clean_df(df)

    df = df.sort_values(["geo", "sex", "time"])

    year, summary = latest_summary(df)
    trend = lt_total_trend(df)
    change_pp = change_over_period(trend)

    summary["distance_to_9%_target_pp (total)"] = summary["total_%"] - settings.target_2030

    summary_path = outdir / "latest_summary.csv"
    trend_path = outdir / "lt_total_trend.csv"
    plot_path = outdir / "trend_lt_vs_eu.png"

    summary.to_excel(outdir / "latest_summary.xlsx", index=False)
    trend.to_excel(outdir / "lt_total_trend.xlsx", index=False)

    plot_lt_vs_eu_total(df, plot_path, settings.target_2030)

    pd.set_option("display.max_columns", 20)
    print("Dataset:", settings.dataset_code)
    print("API endpoint:", settings.endpoint)
    print("Latest year:", year)
    print("\nLatest-year summary:")
    print(summary.to_string(index=False))
    print(
        f"\nLT total change {trend['time'].iloc[0]}→{trend['time'].iloc[-1]}:"
        f" {change_pp:.2f} percentage points"
    )
    print("\nSaved:")
    print(" -", summary_path)
    print(" -", trend_path)
    print(" -", plot_path)


if __name__ == "__main__":
    main()
