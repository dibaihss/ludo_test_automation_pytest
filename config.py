from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _load_dotenv() -> None:
    dotenv_path = Path(__file__).resolve().parent / ".env"
    if not dotenv_path.is_file():
        return

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str = field(
        default_factory=lambda: os.getenv("BASE_URL", "https://strategic.expo.app/")
    )
    browser_name: str = field(default_factory=lambda: os.getenv("BROWSER", "chromium"))
    headless: bool = field(
        default_factory=lambda: os.getenv("HEADLESS", "false").lower() == "true"
    )
    slow_mo: int = field(default_factory=lambda: int(os.getenv("SLOW_MO", "1000")))
    viewport_width: int = field(
        default_factory=lambda: int(os.getenv("VIEWPORT_WIDTH", "1440"))
    )
    viewport_height: int = field(
        default_factory=lambda: int(os.getenv("VIEWPORT_HEIGHT", "1024"))
    )
    screenshot_dir: str = field(
        default_factory=lambda: os.getenv("SCREENSHOT_DIR", "artifacts/screenshots")
    )


def get_settings() -> Settings:
    return Settings()
