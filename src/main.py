from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analysis import change_over_period, latest_summary, lt_total_trend
from src.config import Settings
from src.eurostat_client import fetch_jsonstat
from src.jsonstat import jsonstat_to_df
from src.transform import clean_df
from src.viz import plot_lt_vs_eu_total, plot_lt_absolute_count
from src.population import fetch_lt_population_18_24


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

    latest_xlsx = outdir / "latest_summary.xlsx"
    trend_xlsx = outdir / "lt_total_trend.xlsx"
    plot_path = outdir / "trend_lt_vs_eu.png"

    summary.to_excel(latest_xlsx, index=False)
    trend.to_excel(trend_xlsx, index=False)

    plot_lt_vs_eu_total(df, plot_path, settings.target_2030)

    #sdg_04_10 gives only a percentage rate, so to count an absolute value, I also need the population denominator, and I've load demo_pjan and convert
    pop_year = fetch_lt_population_18_24(settings)

    lt_pct = (
        df[(df["geo"] == "LT") & (df["sex"] == "T")][["time", "value"]]
        .rename(columns={"value": "lt_total_pct"})
        .sort_values("time")
    )

    lt_abs = lt_pct.merge(pop_year, on="time", how="inner")
    if lt_abs.empty:
        raise ValueError("No matching years between sdg_04_10 and demo_pjan for LT.")

    lt_abs["early_leavers_count"] = (
        (lt_abs["lt_total_pct"] / 100.0) * lt_abs["population_18_24"]
    ).round(0).astype(int)

    abs_png = outdir / "lt_early_leavers_absolute.png"
    plot_lt_absolute_count(lt_abs[["time", "early_leavers_count"]], abs_png)

    pd.set_option("display.max_columns", 30)
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
    print(" -", latest_xlsx)
    print(" -", trend_xlsx)
    print(" -", plot_path)
    print(" -", abs_png)


if __name__ == "__main__":
    main()
