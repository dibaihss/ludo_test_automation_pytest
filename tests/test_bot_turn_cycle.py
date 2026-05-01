def test_bots_take_turns_and_blue_can_act_again(offline_game_screen):
    offline_game_screen.skip_tutorial()
    offline_game_screen.dismiss_game_instructions_if_present()

    offline_game_screen.assert_turn_is("blue")

    offline_game_screen.enter_soldier(color="blue")
    offline_game_screen.assert_soldier_visible(2)

    offline_game_screen.wait_for_turn_to_change_from("blue")
    offline_game_screen.wait_for_turn("blue")

    offline_game_screen.enter_soldier(color="blue")
    offline_game_screen.assert_soldier_visible(3)