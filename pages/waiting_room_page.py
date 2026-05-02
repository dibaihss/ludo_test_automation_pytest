from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage
from pages.screen_page import ScreenPage


class WaitingRoomPage(BasePage):
    screen_test_id = "waiting-room-screen"
    heading = "Waiting Room"
    leave_button_test_id = "waiting-room-leave-button"
    add_bot_label = "Add Bot"
    start_game_label = "Start Game"
    player_count_pattern = re.compile(r"Players\s*\((\d+/\d+)\)", re.IGNORECASE)
    match_name_pattern = re.compile(r"Match ID:\s*(.+?)Players\s*\(", re.IGNORECASE)

    @property
    def root(self) -> Locator:
        return self.page.get_by_test_id(self.screen_test_id)

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("WaitingRoom", re.IGNORECASE))
        expect(self.root).to_be_visible()
        expect(self.root.get_by_text(self.heading, exact=True)).to_be_visible()
        expect(self.page.get_by_test_id(self.leave_button_test_id)).to_be_visible()

    def match_name(self) -> str:
        root_text = self.root.text_content() or ""
        match = self.match_name_pattern.search(root_text)
        if match is None:
            raise AssertionError(f"Could not determine match name from {root_text!r}")
        return match.group(1).strip()

    def player_count(self) -> str:
        root_text = self.root.text_content() or ""
        match = self.player_count_pattern.search(root_text)
        if match is None:
            raise AssertionError(f"Could not determine player count from {root_text!r}")
        return match.group(1)

    def wait_for_player_count(self, expected_count: str, timeout_ms: int = 15_000) -> None:
        self.page.wait_for_function(
            """
            ([testId, expectedCount]) => {
                const root = document.querySelector(`[data-testid="${testId}"]`);
                if (!root) {
                    return false;
                }
                const text = root.textContent || "";
                const match = text.match(/Players\s*\((\d+\/\d+)\)/i);
                return !!match && match[1] === expectedCount;
            }
            """,
            arg=[self.screen_test_id, expected_count],
            timeout=timeout_ms,
        )

    def assert_player_visible(self, username: str) -> None:
        expect(self.root.get_by_text(username, exact=True)).to_be_visible()

    def add_bot(self, difficulty: str = "Easy") -> None:
        current_players, max_players = self.player_count().split("/", 1)
        expected_count = f"{int(current_players) + 1}/{max_players}"
        self.root.get_by_text(self.add_bot_label, exact=True).click()
        self.page.get_by_text(difficulty, exact=True).click()
        self.wait_for_player_count(expected_count)

    def add_bots(self, count: int, difficulty: str = "Easy") -> None:
        if count < 1:
            raise ValueError("count must be at least 1")
        for _ in range(count):
            self.add_bot(difficulty)

    def start_game(self) -> ScreenPage:
        self.root.get_by_text(self.start_game_label, exact=True).click()
        screen_page = ScreenPage(self.page, self.base_url)
        screen_page.assert_loaded()
        return screen_page