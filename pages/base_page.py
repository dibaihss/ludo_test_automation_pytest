from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str = "") -> None:
        target = f"{self.base_url}/{path.lstrip('/')}" if path else f"{self.base_url}/"
        self.page.goto(target, wait_until="domcontentloaded")

    def locator_by_text(self, value: str, *, exact: bool = True) -> Locator:
        return self.page.get_by_text(value, exact=exact)

    def click_text(self, value: str, *, exact: bool = True) -> None:
        self.locator_by_text(value, exact=exact).click()

    def expect_text_visible(self, value: str, *, exact: bool = True) -> None:
        expect(self.locator_by_text(value, exact=exact)).to_be_visible()

    def expect_text_hidden(self, value: str, *, exact: bool = True) -> None:
        expect(self.locator_by_text(value, exact=exact)).to_be_hidden()
