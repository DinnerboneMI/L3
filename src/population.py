from __future__ import annotations

import pandas as pd

from src.config import Settings
from src.eurostat_client import fetch_jsonstat
from src.jsonstat import jsonstat_to_df
from src.transform import clean_df


def fetch_lt_population_18_24(settings: Settings) -> pd.DataFrame:
    endpoint = f"{settings.base_url}/demo_pjan"
    ages = ["Y18", "Y19", "Y20", "Y21", "Y22", "Y23", "Y24"]

    params: list[tuple[str, str]] = [("format", "JSON"), ("lang", "EN")]
    params += [("geo", "LT")]
    params += [("sex", "T")]
    params += [("age", a) for a in ages]
    params += [("time", str(y)) for y in settings.years]

    js = fetch_jsonstat(endpoint, params)
    df = jsonstat_to_df(js).dropna(subset=["value"])
    df = clean_df(df)

    pop_year = (
        df.groupby("time", as_index=False)["value"]
        .sum()
        .rename(columns={"value": "population_18_24"})
        .sort_values("time")
    )
    return pop_year
