def test_bots_take_turns_and_blue_can_act_again(play_vs_bot_mode):
    play_vs_bot_mode.skip_tutorial()
    play_vs_bot_mode.dismiss_game_instructions_if_present()

    play_vs_bot_mode.assert_turn_is("blue")

    play_vs_bot_mode.enter_soldier(color="blue")
    play_vs_bot_mode.assert_soldier_visible(2)

    play_vs_bot_mode.wait_for_turn_to_change_from("blue")
    play_vs_bot_mode.wait_for_turn("blue")

    play_vs_bot_mode.enter_soldier(color="blue")
    play_vs_bot_mode.assert_soldier_visible(3)
    
    play_vs_bot_mode.wait_for_turn_to_change_from("blue")
    play_vs_bot_mode.wait_for_turn("blue")
    
    play_vs_bot_mode.move_piece(steps=1, color="blue")
    play_vs_bot_mode.assert_soldier_visible(3)
    play_vs_bot_mode.wait_for_turn_to_change_from("blue")