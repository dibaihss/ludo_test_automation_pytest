import pytest


def test_can_skip_tutorial_on_game_screen(offline_game_screen):
    offline_game_screen.assert_tutorial_visible()
    offline_game_screen.skip_tutorial()
    offline_game_screen.assert_tutorial_dismissed()


def test_game_screen_exposes_soldier_and_move_card_locators(offline_game_screen):
    offline_game_screen.assert_soldier_visible(13)
    for steps in range(1, 7):
        offline_game_screen.assert_move_card_visible(steps, color="blue")


def test_move_piece_rejects_invalid_step_values(offline_game_screen):
    with pytest.raises(ValueError):
        offline_game_screen.move_piece(0)

    with pytest.raises(ValueError):
        offline_game_screen.move_piece(7)


def test_can_enter_new_blue_soldier(offline_game_screen):
    offline_game_screen.skip_tutorial()
    offline_game_screen.dismiss_game_instructions_if_present()
    offline_game_screen.enter_soldier(color="blue")
    offline_game_screen.assert_soldier_visible(2)
