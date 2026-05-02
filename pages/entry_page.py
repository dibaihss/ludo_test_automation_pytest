from __future__ import annotations

import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class EntryPage(BasePage):
    title_text = "Strategic Ludo"
    primary_action = "Play Offline"
    secondary_action = "Continue as Guest"
    guest_name_input_test_id = "guest-name-input"
    confirm_guest_name_button_test_id = "guest-name-confirm-button"


    def open(self) -> None:
        super().open()

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("Login", re.IGNORECASE))
        self.expect_text_visible(self.title_text)
        self.expect_text_visible(self.primary_action)
        self.expect_text_visible(self.secondary_action)

    def start_offline(self) -> None:
        self.click_text(self.primary_action)
        
    def login_as_guest(self) -> None:
        self.click_text(self.secondary_action)
        
    def enter_guest_username(self, username: str) -> None:
        self.page.get_by_test_id(self.guest_name_input_test_id).fill(username)

    def confirm_guest_username(self) -> None:
        self.page.get_by_test_id(self.confirm_guest_name_button_test_id).click()
