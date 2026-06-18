"""
bot.py — Main loop, deduplication, formatting, and Telegram posting.
Fully synchronous. No asyncio, no aiohttp.
"""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone, timedelta

import requests

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    POLL_INTERVAL_SECONDS,
    WEATHER_MAP,
    SEED_EMOJI,
)
from parser import fetch_stock, extract_rotation_id, extract_seeds, extract_weather_key

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

MSK = timezone(timedelta(hours=3))
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


# ─── Formatting ───────────────────────────────────────────────────────────────

def msk_now() -> str:
    return datetime.now(tz=MSK).strftime("%H:%M")


def format_seed_lines(seeds: list[str]) -> str:
    return "\n".join(
        f"• {SEED_EMOJI.get(name, '🌱')} {name}" for name in seeds
    )


def build_seed_post(seeds: list[str]) -> str:
    return (
        "🌷 Seed Stocks\n\n"
        + format_seed_lines(seeds)
        + f"\n\n⏳ time: {msk_now()} MSK\n🌸 @GrowAGarden2Radar"
    )


def build_weather_post(weather_key: str) -> str:
    label = WEATHER_MAP[weather_key]
    return (
        "🫯 Special Weather\n\n"
        f"• Weather - {label}\n\n"
        f"⏳ time: {msk_now()} MSK\n🌸 @GrowAGarden2Radar"
    )


def build_combined_post(seeds: list[str], weather_key: str) -> str:
    label = WEATHER_MAP[weather_key]
    return (
        "🌷 Seed Stocks\n\n"
        + format_seed_lines(seeds)
        + f"\n\n🫯 Weather - {label}\n\n"
        + f"⏳ time: {msk_now()} MSK\n🌸 @GrowAGarden2Radar"
    )


# ─── Telegram ─────────────────────────────────────────────────────────────────

def send_message(text: str) -> None:
    try:
        resp = requests.post(
            TELEGRAM_API,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=15,
        )
        body = resp.json()
        if body.get("ok"):
            log.info("Message sent successfully.")
        else:
            log.error("Telegram error: %s", body)
    except Exception as e:
        log.error("Failed to send message: %s", e)


# ─── Main loop ────────────────────────────────────────────────────────────────

def run_loop() -> None:
    last_rotation_id: str | None = None
    last_weather_key: str | None = None

    log.info("Bot started. Polling every %d seconds.", POLL_INTERVAL_SECONDS)

    while True:
        try:
            data = fetch_stock()

            if data is None:
                log.warning("API fetch failed — skipping cycle.")
            else:
                rotation_id = extract_rotation_id(data)
                seeds = extract_seeds(data)
                weather_key = extract_weather_key(data)

                seeds_changed = (rotation_id is not None) and (rotation_id != last_rotation_id)
                weather_changed = (weather_key is not None) and (weather_key != last_weather_key)

                if seeds_changed and not seeds:
                    log.info("Seed post skipped (empty seeds). rotation=%s", rotation_id)
                    last_rotation_id = rotation_id
                    seeds_changed = False

                if seeds_changed and weather_changed:
                    log.info("Combined post: rotation=%s weather=%s seeds=%s", rotation_id, weather_key, seeds)
                    send_message(build_combined_post(seeds, weather_key))
                    last_rotation_id = rotation_id
                    last_weather_key = weather_key
                elif seeds_changed:
                    log.info("Seed post: rotation=%s seeds=%s", rotation_id, seeds)
                    send_message(build_seed_post(seeds))
                    last_rotation_id = rotation_id
                elif weather_changed:
                    log.info("Weather post: weather=%s", weather_key)
                    send_message(build_weather_post(weather_key))
                    last_weather_key = weather_key
                else:
                    log.info("No change. rotation=%s weather=%s", rotation_id, weather_key)

        except Exception as e:
            log.error("Unexpected error in main loop: %s", e)

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_loop()
