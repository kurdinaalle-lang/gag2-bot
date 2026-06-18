"""
parser.py — API fetching and data extraction only.
No business logic, no posting, no state.
"""
from __future__ import annotations

import aiohttp
from typing import Optional

from config import STOCK_API_URL, SEED_WHITELIST, WEATHER_MAP


async def fetch_stock() -> Optional[dict]:
    """Fetch raw stock data from the API. Returns None on any error."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(STOCK_API_URL, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return None
                return await resp.json()
    except Exception:
        return None


def extract_rotation_id(data: dict) -> Optional[str]:
    """Return the rotation id string, or None if missing."""
    return str(data.get("rotation", {}).get("id", "")) or None


def extract_seeds(data: dict) -> list[str]:
    """
    Return whitelisted seed names present in the current stock.
    Guarantees deterministic ordering (sorted).
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
    Return the lowercase weather type ONLY if it is in WEATHER_MAP.
    Returns None for anything else (Rain, Snow, Clear, Night, etc.).
    """
    raw_type: str = data.get("stock", {}).get("weather", {}).get("type", "") or ""
    normalized = raw_type.strip().lower()
    if normalized in WEATHER_MAP:
        return normalized
    return None
