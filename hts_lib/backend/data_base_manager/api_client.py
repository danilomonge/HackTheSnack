"""Small HTTP client shared by the HackTheSnackDB managers.

* Builds URLs from the base URL resolved by ``db_config``.
* Always passes query parameters through httpx so names such as
  ``"M&M'S"`` or ``"Crème fraîche"`` are URL-encoded correctly.
* Uses timeouts long enough to survive a cold start of the free Render
  instance (the first request after ~15 idle minutes can take ~1 minute).

Works the same on desktop (CPython) and in the browser (Pyodide), where httpx
requests are executed through the browser's networking stack.
"""

from __future__ import annotations

import threading

import httpx

from backend.data_base_manager.db_config import IS_WEB, get_user_management_url

#: Timeout for requests that may hit a sleeping Render instance.
REQUEST_TIMEOUT = 90.0
#: Timeout for the quick "is the database reachable?" probe.
PROBE_TIMEOUT = 90.0

JSON_HEADERS = {"Content-Type": "application/json"}


def url(path: str) -> str:
    """Absolute URL of an API path such as ``/product/detail``."""
    return f"{get_user_management_url()}/{path.lstrip('/')}"


def get(path: str, params: dict | None = None, timeout: float = REQUEST_TIMEOUT) -> httpx.Response:
    return httpx.get(url(path), params=params, timeout=timeout)


def post(path: str, payload: dict, timeout: float = REQUEST_TIMEOUT) -> httpx.Response:
    return httpx.post(url(path), json=payload, headers=JSON_HEADERS, timeout=timeout)


def delete(path: str, params: dict | None = None, timeout: float = REQUEST_TIMEOUT) -> httpx.Response:
    return httpx.delete(url(path), params=params, timeout=timeout)


def json_data(response: httpx.Response, default=None):
    """Returns ``response.json()["data"]`` or ``default`` if it is missing or invalid."""
    try:
        payload = response.json()
    except ValueError:
        return default
    if not isinstance(payload, dict):
        return default
    data = payload.get("data")
    return default if data is None else data


def warm_up(*urls: str) -> None:
    """Fire-and-forget GET requests that wake sleeping free-tier services.

    Called once when the app starts so the API is usually awake by the time
    the user clicks Search or Save. Never raises and never blocks the UI.
    """
    targets = [u for u in urls if u]
    if not targets:
        return

    if IS_WEB:
        try:
            import js  # type: ignore[import-not-found]  # Pyodide bridge to the browser

            # Runs entirely in JavaScript: a "no-cors" request still reaches (and
            # wakes) the service, the opaque response is ignored, and errors are
            # caught there, so no rejected promise reaches Python and nothing is
            # logged to the console. (Spring's actuator endpoints send no CORS headers.)
            ping = js.Function.new(
                "url",
                "fetch(url, { mode: 'no-cors', cache: 'no-store' }).catch(function () {});",
            )
            for target in targets:
                ping(target)
        except Exception:
            pass
        return

    def _ping():
        for target in targets:
            try:
                httpx.get(target, timeout=REQUEST_TIMEOUT)
            except Exception:
                pass

    threading.Thread(target=_ping, daemon=True).start()
