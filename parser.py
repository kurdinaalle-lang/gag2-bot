"""
parser.py — API fetching and data extraction only.
Pure synchronous. No business logic, no posting, no state.
"""
from __future__ import annotations

from typing import Optional

import requests

from config import STOCK_API_URL, SEED_WHITELIST, WEATHER_MAP


def fetch_stock() -> Optional[dict]:
    """Fetch raw stock data. Returns None on any error."""
    try:
        r = requests.get(
            STOCK_API_URL,
            timeout=15,
            headers={"User-Agent": "GrowAGarden2Bot/1.0"},
        )
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def extract_rotation_id(data: dict) -> Optional[str]:
    """Return rotation id as string, or None if missing."""
    raw = data.get("rotation", {}).get("id")
    return str(raw) if raw is not None else None


def extract_seeds(data: dict) -> list[str]:
    """
    Return whitelisted seed names from the current stock.
    Sorted for deterministic output.
    """
    raw_seeds: list = data.get("stock", {}).get("seeds", []) or []
    result = []
    for seed in raw_seeds:
        name = seed.get("name", "") if isinstance(seed, dict) else str(seed)
        if name in SEED_WHITELIST:
            result.append(name)
    return sorted(result)


def extract_weather_key(data: dict) -> Optional[str]:
    """
    Return lowercase weather type ONLY if it is in WEATHER_MAP.
    Returns None for Rain, Snow, Clear, Night, or anything not in the list.
    """
    raw: str = data.get("stock", {}).get("weather", {}).get("type", "") or ""
    normalized = raw.strip().lower()
    return normalized if normalized in WEATHER_MAP else None
