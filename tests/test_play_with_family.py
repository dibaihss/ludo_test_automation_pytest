def test_play_with_family_mode(play_with_family_mode):
    play_with_family_mode.dismiss_game_instructions_if_present()

    play_with_family_mode.assert_turn_is("blue")

    play_with_family_mode.enter_soldier(color="blue")
    play_with_family_mode.assert_soldier_visible(2)
    
    play_with_family_mode.assert_turn_is("green")
    
    play_with_family_mode.enter_soldier(color="green")
    play_with_family_mode.assert_soldier_visible(14)
    
    play_with_family_mode.assert_turn_is("red")
    
    play_with_family_mode.move_piece(steps=2, color="red")
    play_with_family_mode.assert_soldier_visible(5)
    
    play_with_family_mode.assert_turn_is("pink")
    
    play_with_family_mode.move_piece(steps=3, color="yellow")
    play_with_family_mode.assert_soldier_visible(9)

    # play_with_family_mode.wait_for_turn_to_change_from("blue")
    # play_with_family_mode.wait_for_turn("blue")

    # play_with_family_mode.enter_soldier(color="blue")
    # play_with_family_mode.assert_soldier_visible(3)
    
    # play_with_family_mode.wait_for_turn_to_change_from("blue")
    # play_with_family_mode.wait_for_turn("blue")
    
    # play_with_family_mode.move_piece(steps=1, color="blue")
    # play_with_family_mode.assert_soldier_visible(3)