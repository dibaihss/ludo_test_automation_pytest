from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class HomePage(BasePage):
    app_title = "Strategic Ludo"
    heading = "Dashboard"
    play_offline_label = "Play Offline"
    options_heading = "Offline Play Options"
    bot_option = "Play vs Bot"

    @property
    def root(self) -> Locator:
        return self.page.get_by_test_id("home-screen")

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("Home", re.IGNORECASE))
        expect(self.root).to_be_visible()
        expect(self.root.get_by_text(self.app_title, exact=True)).to_be_visible()
        expect(self.root.get_by_text(self.heading, exact=True)).to_be_visible()
        expect(self.root.get_by_text(self.play_offline_label, exact=True)).to_be_visible()

    def open_offline_options(self) -> None:
        self.root.get_by_text(self.play_offline_label, exact=True).click()
        self.expect_text_visible(self.options_heading)

    def choose_play_vs_bot(self) -> None:
        self.click_text(self.bot_option)
        self.expect_text_visible("Choose bot difficulty")

    def choose_bot_difficulty(self, difficulty: str) -> None:
        self.click_text(difficulty)

    def start_offline_vs_bot(self, difficulty: str = "Easy") -> None:
        self.open_offline_options()
        self.choose_play_vs_bot()
        self.choose_bot_difficulty(difficulty)
