from __future__ import annotations

from typing import Dict, List, Tuple

import requests


def fetch_jsonstat(url: str, params: List[Tuple[str, str]]) -> Dict:
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    return response.json()
