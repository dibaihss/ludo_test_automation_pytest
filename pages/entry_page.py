from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class EntryPage(BasePage):
    title_text = "Strategic Ludo"
    primary_action = "Play Offline"
    secondary_action = "Continue as Guest"

    def open(self) -> None:
        super().open()

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("Login", re.IGNORECASE))
        self.expect_text_visible(self.title_text)
        self.expect_text_visible(self.primary_action)
        self.expect_text_visible(self.secondary_action)

    def start_offline(self) -> None:
        self.click_text(self.primary_action)
