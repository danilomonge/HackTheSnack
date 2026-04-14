"""Configures the FakeTheSnackDB API base URL.

Priority order:
  1. Environment variable  USER_MANAGEMENT_BASE_URL  (local dev / CI)
  2. runtime-config.json fetched from the same origin as the page (web/Pyodide)
  3. assets/runtime-config.json on disk (local Flet desktop run)
  4. Hard-coded localhost fallback (local dev without any config file)

Call initialize_db_url(page) once at app start (in hts_lib/main.py)
before any manager is used.
"""

import json
import os
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit

import httpx

IS_WEB: bool = sys.platform == "emscripten"

# Base directory is two levels up from this file: hts_lib/
_HTS_LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_RUNTIME_CONFIG_PATH = os.path.join(_HTS_LIB_DIR, "assets", "runtime-config.json")

_DEFAULT_URL = "http://localhost:8087/user-management"

_cached_url: str | None = None


def _build_same_origin_asset_url(page, asset_name: str) -> str | None:
    """Build an absolute URL to an asset based on the current page URL."""
    page_url = getattr(page, "url", None)
    if not page_url:
        return None
    parsed = urlsplit(page_url)
    path = parsed.path or "/"
    if not path.endswith("/"):
        path = path.rsplit("/", 1)[0] + "/"
    base_url = urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))
    return urljoin(base_url, asset_name)


def initialize_db_url(page=None) -> None:
    """Resolve and cache the FakeTheSnackDB base URL.

    Call this once from hts_lib/main.py, passing the Flet page object.
    """
    global _cached_url

    # 1. Environment variable (works in local dev and on native builds)
    env_url = os.environ.get("USER_MANAGEMENT_BASE_URL", "").strip().rstrip("/")
    if env_url:
        _cached_url = env_url
        return

    # 2. runtime-config.json fetched via HTTP when running in browser (Pyodide)
    if IS_WEB and page is not None:
        config_url = _build_same_origin_asset_url(page, "runtime-config.json")
        if config_url:
            try:
                response = httpx.get(config_url, timeout=5.0)
                response.raise_for_status()
                data = response.json()
                url = str(data.get("user_management_url", "")).strip().rstrip("/")
                if url:
                    _cached_url = url
                    return
            except Exception:
                pass

    # 3. assets/runtime-config.json on disk (local desktop run)
    if not IS_WEB and os.path.exists(_RUNTIME_CONFIG_PATH):
        try:
            with open(_RUNTIME_CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            url = str(data.get("user_management_url", "")).strip().rstrip("/")
            if url:
                _cached_url = url
                return
        except Exception:
            pass

    # 4. Default localhost fallback
    _cached_url = _DEFAULT_URL


def get_user_management_url() -> str:
    """Return the base URL for the FakeTheSnackDB API (no trailing slash).

    Initializes with the default if initialize_db_url() was never called.
    """
    if _cached_url is None:
        initialize_db_url()
    return _cached_url  # type: ignore[return-value]
