"""Utility functions for the core module."""

import json
import time
from typing import Optional
from ctypes import windll, create_unicode_buffer


def get_foreground_window() -> Optional[str]:
    """
    Get the title of the foreground window.
    """
    active_window_handle = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(active_window_handle)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(active_window_handle, buf, length + 1)

    return buf.value if buf.value else None


def load_app_shortcuts(config_file: str) -> dict:
    """Load application configuration from a JSON file."""
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)


def wait_for_window(
    app, wait_time: float = 20.0, retry_interval: float = 1.0, title_re: str = None
):
    """Wait until at least one window (even hidden) is available, then return it."""
    elapsed = 0.0
    while elapsed < wait_time:
        try:
            # Retrieve all top-level windows including hidden ones.
            if title_re:
                windows = app.windows(visible_only=False, title_re=title_re)
            else:
                windows = app.windows(visible_only=False)
            if windows:
                window = windows[0]
                print(f"Window found: {window.window_text()}")  # Debug
                return window
        except Exception:
            pass
        time.sleep(retry_interval)
        elapsed += retry_interval
        print(f"Waiting for window... ({elapsed:.1f}s)")  # Debug
    raise TimeoutError(f"No window found after {wait_time} seconds.")
