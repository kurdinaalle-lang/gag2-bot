import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "@GrowAGarden2Radar")

STOCK_API_URL = "https://api.growagarden2wiki.net/api/v1/games/grow-a-garden-2/stock"

POLL_INTERVAL_SECONDS = 300

BLOCKED_SEEDS = {
    "Carrot",
    "Strawberry",
    "Blueberry",
    "Tulip",
    "Tomato",
    "Apple",
    "Bamboo",
    "Corn",
    "Cactus",
    "Pineapple",
    "Amanita",
    "Green Bean",
    "Banana",
    "Grape",
    "Rope",
    "Mango",
    "Dragon Fruit",
}

WEATHER_MAP = {
    "rainbow":   "🌈 Rainbow",
    "bloodmoon": "🩸 Blood Moon",
    "storm":     "⛈️ Storm",
    "sandstorm": "🌪️ Sandstorm",
    "starfall":  "🌠 Starfall",
    "lightning": "⚡ Lightning",
}

SEED_EMOJI = {
    "Acorn":          "🌰",
    "Cherry":         "🍒",
    "Sunflower":      "🌻",
    "Venus Fly Trap": "🪤",
    "Pomegranate":    "🍎",
    "Poison Apple":   "🍏",
    "Moon Bloom":     "🌸",
    "Dragon's Breath":"🔥",
}
