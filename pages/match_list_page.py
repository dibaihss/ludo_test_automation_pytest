from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage
from pages.waiting_room_page import WaitingRoomPage


class MatchListPage(BasePage):
    screen_test_id = "match-list-screen"
    heading = "Available Matches"
    create_button_test_id = "match-list-create-button"

    @property
    def root(self) -> Locator:
        return self.page.get_by_test_id(self.screen_test_id)

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("MatchList", re.IGNORECASE))
        expect(self.root).to_be_visible()
        expect(self.root.get_by_text(self.heading, exact=True)).to_be_visible()
        expect(self.page.get_by_test_id(self.create_button_test_id)).to_be_visible()

    def create_match(self) -> WaitingRoomPage:
        self.page.get_by_test_id(self.create_button_test_id).click()
        waiting_room_page = WaitingRoomPage(self.page, self.base_url)
        waiting_room_page.assert_loaded()
        return waiting_room_page

    def match_item(self, match_name: str) -> Locator:
        return self.root.get_by_text(match_name, exact=True).locator("..").locator("..")

    def join_match(self, match_name: str) -> WaitingRoomPage:
        self.match_item(match_name).click()
        waiting_room_page = WaitingRoomPage(self.page, self.base_url)
        waiting_room_page.assert_loaded()
        return waiting_room_page