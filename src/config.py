from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Settings:
    dataset_code: str = "sdg_04_10"
    base_url: str = (
        "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
    )
    years: List[int] = None  # type: ignore[assignment]
    geos: List[str] = None   # type: ignore[assignment]
    sexes: List[str] = None  # type: ignore[assignment]
    target_2030: float = 9.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "years", list(range(2015, 2025)))
        object.__setattr__(self, "geos", ["LT", "EU27_2020"])
        object.__setattr__(self, "sexes", ["T", "M", "F"])

    @property
    def endpoint(self) -> str:
        return f"{self.base_url}/{self.dataset_code}"
