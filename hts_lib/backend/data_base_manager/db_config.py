"""Runtime configuration: where the HackTheSnackDB API (and its nutrition endpoints) live.

Both URLs come from ``assets/runtime-config.json``::

    {
      "user_management_url": "https://fakethesnackdb-api.onrender.com/user-management",
      "nutrition_proxy_url": "https://fakethesnackdb-api.onrender.com/user-management"
    }

Resolution order for each value:
  1. Environment variable (``USER_MANAGEMENT_BASE_URL`` / ``NUTRITION_PROXY_URL``),
     handy for local development and tests.
  2. ``runtime-config.json`` served next to the web app (browser / Pyodide build).
  3. ``assets/runtime-config.json`` on disk (desktop run).
  4. Defaults: a local API on ``http://localhost:8087/user-management`` and no proxy.

Call ``initialize_db_url(page)`` once at start-up (done in ``hts_lib/main.py``);
the file is read only once and cached.
"""

from __future__ import annotations

import json
import os
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx

IS_WEB: bool = sys.platform == "emscripten"

# hts_lib/ is two levels up from this file.
_HTS_LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_RUNTIME_CONFIG_PATH = os.path.join(_HTS_LIB_DIR, "assets", "runtime-config.json")

_DEFAULT_URL = "http://localhost:8087/user-management"

_cached_config: dict | None = None
_cached_url: str | None = None


def _normalize_url(value) -> str:
    return str(value or "").strip().rstrip("/")


def _build_same_origin_asset_url(page, asset_name: str) -> str | None:
    """Absolute URL of an asset that sits next to the current page."""
    page_url = getattr(page, "url", None)
    if not page_url:
        return None
    parsed = urlsplit(page_url)
    path = parsed.path or "/"
    if not path.endswith("/"):
        path = path.rsplit("/", 1)[0] + "/"
    base_url = urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))
    return urljoin(base_url, asset_name)


def _read_runtime_config(page=None) -> dict:
    """Reads runtime-config.json from the web server (browser) or from disk (desktop)."""
    if IS_WEB and page is not None:
        config_url = _build_same_origin_asset_url(page, "runtime-config.json")
        if config_url:
            try:
                response = httpx.get(config_url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, dict):
                    return data
            except Exception:
                pass

    if os.path.exists(_RUNTIME_CONFIG_PATH):
        try:
            with open(_RUNTIME_CONFIG_PATH, "r", encoding="utf-8") as config_file:
                data = json.load(config_file)
            if isinstance(data, dict):
                return data
        except Exception:
            pass

    return {}


def get_runtime_config(page=None) -> dict:
    """Returns the (cached) contents of runtime-config.json."""
    global _cached_config
    if _cached_config is None:
        _cached_config = _read_runtime_config(page)
    return _cached_config


def initialize_db_url(page=None) -> None:
    """Resolves and caches the API base URL. Call once from hts_lib/main.py."""
    global _cached_url

    env_url = _normalize_url(os.environ.get("USER_MANAGEMENT_BASE_URL"))
    if env_url:
        _cached_url = env_url
        return

    _cached_url = _normalize_url(get_runtime_config(page).get("user_management_url")) or _DEFAULT_URL


def get_user_management_url() -> str:
    """Base URL of the HackTheSnackDB API, without trailing slash."""
    if _cached_url is None:
        initialize_db_url()
    return _cached_url  # type: ignore[return-value]


def get_nutrition_proxy_url(page=None) -> str:
    """Base URL serving ``/api/nutrition`` and ``/api/translate`` (normally the API), or "" if none."""
    env_url = _normalize_url(os.environ.get("NUTRITION_PROXY_URL"))
    if env_url:
        return env_url
    return _normalize_url(get_runtime_config(page).get("nutrition_proxy_url"))


def reset_cache() -> None:
    """Forgets the cached configuration (used by tests)."""
    global _cached_config, _cached_url
    _cached_config = None
    _cached_url = None
