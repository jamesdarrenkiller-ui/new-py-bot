import json
import os
from dataclasses import dataclass
from typing import Any


def _csv(name: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, "").split(",") if item.strip()]


def _json(name: str, default: Any) -> Any:
    raw = os.getenv(name, "")
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default


@dataclass(frozen=True)
class Settings:
    token: str
    owner_id: int
    prefix: str
    mongodb_uri: str | None
    spotify_client_id: str | None
    spotify_client_secret: str | None
    groq_api_keys: list[str]
    tmdb_api_key: str | None
    twitter_token: str | None
    openweather_api_key: str | None
    giphy_api_key: str | None
    memer_api_key: str | None
    ksoft_api_key: str | None
    yandex_api_key: str | None
    coingecko_api_key: str | None
    lavalink_nodes: list[dict[str, Any]]


def load_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN", "")
    owner_id_raw = os.getenv("BOT_OWNER_ID", "0")
    if not token:
        raise RuntimeError("DISCORD_TOKEN is not configured")
    try:
        owner_id = int(owner_id_raw)
    except ValueError as exc:
        raise RuntimeError("BOT_OWNER_ID must be an integer") from exc
    if owner_id <= 0:
        raise RuntimeError("BOT_OWNER_ID must be configured")

    return Settings(
        token=token,
        owner_id=owner_id,
        prefix=os.getenv("PREFIX", "."),
        mongodb_uri=os.getenv("MONGODB_URI") or None,
        spotify_client_id=os.getenv("SPOTIFY_CLIENT_ID") or None,
        spotify_client_secret=os.getenv("SPOTIFY_CLIENT_SECRET") or None,
        groq_api_keys=_csv("GROQ_API_KEYS"),
        tmdb_api_key=os.getenv("TMDB_API_KEY") or None,
        twitter_token=os.getenv("TWITTER_TOKEN") or None,
        openweather_api_key=os.getenv("OPENWEATHER_API_KEY") or None,
        giphy_api_key=os.getenv("GIPHY_API_KEY") or None,
        memer_api_key=os.getenv("MEMER_API_KEY") or None,
        ksoft_api_key=os.getenv("KSOFT_API_KEY") or None,
        yandex_api_key=os.getenv("YANDEX_API_KEY") or None,
        coingecko_api_key=os.getenv("COINGECKO_API_KEY") or None,
        lavalink_nodes=_json("LAVALINK_NODES_JSON", []),
    )
