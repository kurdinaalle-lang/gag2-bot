"""
parser.py — API fetching and data extraction only.
"""

from typing import Optional
import requests

from config import STOCK_API_URL, WEATHER_MAP, BLOCKED_SEEDS


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
    try:
        return data.get("rotation", {}).get("id")
    except Exception:
        return None


def extract_seeds(data: dict) -> list[str]:
    try:
        raw_seeds = data.get("stock", {}).get("seeds", []) or []

        result = []

        for seed in raw_seeds:
            name = seed.get("name", "") if isinstance(seed, dict) else str(seed)
            name = name.strip()

            if not name:
                continue

            # ❌ фильтр ненужных семян
            if name in BLOCKED_SEEDS:
                continue

            result.append(name)

        # убираем дубликаты
        return sorted(set(result))

    except Exception as e:
        print("SEEDS ERROR:", repr(e))
        return []


def extract_weather_key(data: dict) -> Optional[str]:
    try:
        raw_type = data.get("stock", {}).get("weather", {}).get("type", "")
        normalized = raw_type.strip().lower()

        if normalized in WEATHER_MAP:
            return normalized

        return None

    except Exception:
        return None
