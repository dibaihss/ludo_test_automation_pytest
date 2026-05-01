from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://strategic.expo.app/")
    browser_name: str = os.getenv("BROWSER", "chromium")
    headless: bool = os.getenv("HEADLESS", "false").lower() == "true"
    slow_mo: int = int(os.getenv("SLOW_MO", "500"))
    viewport_width: int = int(os.getenv("VIEWPORT_WIDTH", "1440"))
    viewport_height: int = int(os.getenv("VIEWPORT_HEIGHT", "1024"))
    screenshot_dir: str = os.getenv("SCREENSHOT_DIR", "artifacts/screenshots")


def get_settings() -> Settings:
    return Settings()
