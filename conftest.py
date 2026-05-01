from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config import Settings, get_settings
from pages.entry_page import EntryPage
from pages.home_page import HomePage
from pages.screen_page import ScreenPage


def _sanitize_node_id(node_id: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in node_id)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session")
def playwright_instance() -> Iterator[Playwright]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Iterator[Browser]:
    browser_factory = getattr(playwright_instance, settings.browser_name)
    browser = browser_factory.launch(headless=settings.headless, slow_mo=settings.slow_mo)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser, settings: Settings) -> Iterator[BrowserContext]:
    context = browser.new_context(
        viewport={"width": settings.viewport_width, "height": settings.viewport_height}
    )
    context.set_default_timeout(15_000)
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Iterator[Page]:
    page = context.new_page()
    request.node._playwright_page = page
    yield page
    page.close()


@pytest.fixture()
def offline_game_screen(page: Page, settings: Settings) -> ScreenPage:
    entry_page = EntryPage(page, settings.base_url)
    home_page = HomePage(page, settings.base_url)
    screen_page = ScreenPage(page, settings.base_url)

    entry_page.open()
    entry_page.assert_loaded()
    entry_page.start_offline()
    home_page.assert_loaded()
    home_page.start_offline_vs_bot(difficulty="Easy")
    screen_page.assert_loaded()

    return screen_page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return

    page = getattr(item, "_playwright_page", None)
    if page is None:
        return

    settings = get_settings()
    screenshot_dir = Path(settings.screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{_sanitize_node_id(item.nodeid)}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
