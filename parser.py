"""
parser.py — API fetching and data extraction only.
"""

from typing import Optional
import requests

from config import STOCK_API_URL, SEED_WHITELIST, WEATHER_MAP

def fetch_stock() -> Optional[dict]:
    try:
        print("TRY FETCH...")

        r = requests.get(
            STOCK_API_URL,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return None

        return r.json()

    except Exception as e:
        print("FETCH ERROR:", repr(e))
        return None

def extract_rotation_id(data: dict) -> Optional[str]:
    return data.get("rotation", {}).get("id")

    def extract_seeds(data: dict) -> list[str]:
        raw_seeds = data.get("stock", {}).get("seeds", []) or []

        result = []
        for seed in raw_seeds:
            name = seed.get("name", "") if isinstance(seed, dict) else str(seed)
            print("SEED FROM API:", repr(name))  # важно
            result.append(name.strip())

        return result
    raw_seeds = data.get("stock", {}).get("seeds", []) or []

    result = []
    for seed in raw_seeds:
        name = seed.get("name", "") if isinstance(seed, dict) else str(seed)
        name = name.strip()

        if name in SEED_WHITELIST:
            result.append(name)

    return sorted(result)

def extract_weather_key(data: dict) -> Optional[str]:
    raw_type = data.get("stock", {}).get("weather", {}).get("type", "")
    normalized = raw_type.strip().lower()

    if normalized in WEATHER_MAP:
        return normalized

    return None