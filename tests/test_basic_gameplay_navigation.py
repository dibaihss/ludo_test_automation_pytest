import pytest


def test_can_skip_tutorial_on_game_screen(play_vs_bot_mode):
    play_vs_bot_mode.assert_tutorial_visible()
    play_vs_bot_mode.skip_tutorial()
    play_vs_bot_mode.assert_tutorial_dismissed()


def test_game_screen_exposes_soldier_and_move_card_locators(play_vs_bot_mode):
    play_vs_bot_mode.assert_soldier_visible(13)
    for steps in range(1, 7):
        play_vs_bot_mode.assert_move_card_visible(steps, color="blue")


def test_move_piece_rejects_invalid_step_values(play_vs_bot_mode):
    with pytest.raises(ValueError):
        play_vs_bot_mode.move_piece(0)

    with pytest.raises(ValueError):
        play_vs_bot_mode.move_piece(7)


def test_can_enter_new_blue_soldier(play_vs_bot_mode):
    play_vs_bot_mode.skip_tutorial()
    play_vs_bot_mode.dismiss_game_instructions_if_present()
    play_vs_bot_mode.enter_soldier(color="blue")
    play_vs_bot_mode.assert_soldier_visible(2)
