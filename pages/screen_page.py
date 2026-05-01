from __future__ import annotations

import re

from playwright.sync_api import Locator, expect

from pages.base_page import BasePage


class ScreenPage(BasePage):
    game_screen_test_id = "game-screen"
    turn_color_pattern = re.compile(
        r"Time:\s*\d+s[^a-z]*(red|blue|yellow|green)", re.IGNORECASE
    )
    tutorial_title = "Select a soldier"
    tutorial_dismiss = "Skip tutorial"
    turn_action = "skip my turn"
    exit_action = "Exit"

    @property
    def root(self) -> Locator:
        return self.page.get_by_test_id(self.game_screen_test_id)

    def soldier(self, soldier_id: int) -> Locator:
        if soldier_id < 1:
            raise ValueError("soldier_id must be a positive integer")
        return self.page.get_by_test_id(f"soldier-{soldier_id}")

    def move_card(self, steps: int, *, color: str = "blue") -> Locator:
        if steps not in range(1, 7):
            raise ValueError("steps must be between 1 and 6")
        return self.page.get_by_test_id(f"move-card-{color.lower()}-{steps}")

    def enter_soldier_button(self, *, color: str = "blue") -> Locator:
        return self.page.get_by_test_id(f"enter-soldier-{color.lower()}")

    def skip_turn_button(self) -> Locator:
        return self.page.get_by_test_id("game-skip-turn-button")

    def exit_button(self) -> Locator:
        return self.page.get_by_test_id("game-exit-button")

    def current_turn_color(self) -> str:
        root_text = self.root.text_content() or ""
        match = self.turn_color_pattern.search(root_text)
        if match is None:
            raise AssertionError(f"Could not determine turn color from {root_text!r}")
        return match.group(1).lower()

    def assert_turn_is(self, color: str) -> None:
        expected_color = color.lower()
        actual_color = self.current_turn_color()
        assert actual_color == expected_color, (
            f"Expected turn to be {expected_color}, but got {actual_color}"
        )

    def wait_for_turn(self, color: str, timeout_ms: int = 45_000) -> None:
        expected_color = color.lower()
        self.page.wait_for_function(
            """
            ([testId, expectedColor]) => {
                const root = document.querySelector(`[data-testid="${testId}"]`);
                if (!root) {
                    return false;
                }
                const text = root.textContent || "";
                const match = text.match(/Time:\s*\d+s[^A-Za-z]*(red|blue|yellow|green)/i);
                return !!match && match[1].toLowerCase() === expectedColor;
            }
            """,
            arg=[self.game_screen_test_id, expected_color],
            timeout=timeout_ms,
        )

    def wait_for_turn_to_change_from(self, color: str, timeout_ms: int = 15_000) -> None:
        original_color = color.lower()
        self.page.wait_for_function(
            """
            ([testId, originalColor]) => {
                const root = document.querySelector(`[data-testid="${testId}"]`);
                if (!root) {
                    return false;
                }
                const text = root.textContent || "";
                const match = text.match(/Time:\s*\d+s[^A-Za-z]*(red|blue|yellow|green)/i);
                return !!match && match[1].toLowerCase() !== originalColor;
            }
            """,
            arg=[self.game_screen_test_id, original_color],
            timeout=timeout_ms,
        )

    def assert_loaded(self) -> None:
        expect(self.page).to_have_title(re.compile("Game", re.IGNORECASE))
        expect(self.root).to_be_visible()
        expect(self.skip_turn_button()).to_be_visible()
        expect(self.exit_button()).to_be_visible()
        self.expect_text_visible(self.tutorial_title)

    def assert_tutorial_visible(self) -> None:
        self.expect_text_visible(self.tutorial_title)
        self.expect_text_visible(self.tutorial_dismiss)

    def assert_tutorial_step_visible(self, title: str) -> None:
        self.expect_text_visible(title)

    def skip_tutorial(self) -> None:
        self.page.get_by_test_id("tutorial-skip-button").click()

    def dismiss_game_instructions_if_present(self) -> None:
        got_it_button = self.page.get_by_text("Got it", exact=True)
        if got_it_button.count() > 0:
            got_it_button.last.click(force=True)

    def assert_tutorial_dismissed(self) -> None:
        self.expect_text_hidden(self.tutorial_title)
        self.expect_text_hidden(self.tutorial_dismiss)

    def assert_soldier_visible(self, soldier_id: int) -> None:
        expect(self.soldier(soldier_id)).to_be_visible()

    def select_soldier(self, soldier_id: int) -> None:
        self.soldier(soldier_id).click()

    def assert_move_card_visible(self, steps: int, *, color: str = "blue") -> None:
        expect(self.move_card(steps, color=color)).to_be_visible()

    def move_piece(self, steps: int, *, color: str = "blue") -> None:
        self.move_card(steps, color=color).click()

    def enter_soldier(self, *, color: str = "blue") -> None:
        self.enter_soldier_button(color=color).click()

    def skip_turn(self) -> None:
        self.skip_turn_button().click()

    def exit_game(self) -> None:
        self.exit_button().click()
