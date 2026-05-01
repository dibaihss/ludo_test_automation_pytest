from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class ScreenPage(BasePage):
    tutorial_title = "Select a soldier"
    tutorial_dismiss = "Skip tutorial"
    turn_action = "skip my turn"
    exit_action = "Exit"

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("Game", re.IGNORECASE))
        self.expect_text_visible(self.turn_action)
        self.expect_text_visible(self.exit_action)
        self.expect_text_visible(self.tutorial_title)

    def assert_tutorial_visible(self) -> None:
        self.expect_text_visible(self.tutorial_title)
        self.expect_text_visible(self.tutorial_dismiss)

    def skip_tutorial(self) -> None:
        self.click_text(self.tutorial_dismiss)

    def assert_tutorial_dismissed(self) -> None:
        self.expect_text_hidden(self.tutorial_title)
        self.expect_text_hidden(self.tutorial_dismiss)
