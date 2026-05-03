from pages.screen_page import ScreenPage


def test_guest_player_can_create_and_one_guest_can_join(two_online_players):
    host_home_page, guest_home_page, _, _ = two_online_players

    host_match_list = host_home_page.open_multiplayer()
    host_waiting_room = host_match_list.create_match()
    match_name = host_waiting_room.match_name()

    guest_match_list = guest_home_page.open_multiplayer()
    guest_waiting_room = guest_match_list.join_match(match_name)

    host_waiting_room.wait_for_player_count("2/4")
    guest_waiting_room.wait_for_player_count("2/4")
    host_waiting_room.add_bots(2)
    host_waiting_room.wait_for_player_count("4/4")
    guest_waiting_room.wait_for_player_count("4/4")
    assert host_waiting_room.match_name() == match_name
    assert guest_waiting_room.match_name() == match_name

    host_game_screen = host_waiting_room.start_game()
    guest_game_screen = ScreenPage(guest_waiting_room.page, guest_waiting_room.base_url)
    guest_game_screen.assert_loaded()
    assert host_game_screen.current_turn_color() in {"red", "blue", "pink", "green"}
    
def test_guest_player_can_create_and_two_guests_can_join(three_online_players):
    host_home_page, guest_home_page, second_guest_home_page, _, _, _ = three_online_players

    host_match_list = host_home_page.open_multiplayer()
    host_waiting_room = host_match_list.create_match()
    match_name = host_waiting_room.match_name()

    guest_match_list = guest_home_page.open_multiplayer()
    guest_waiting_room = guest_match_list.join_match(match_name)
    
    second_guest_match_list = second_guest_home_page.open_multiplayer()
    second_guest_waiting_room = second_guest_match_list.join_match(match_name)

    host_waiting_room.wait_for_player_count("3/4")
    guest_waiting_room.wait_for_player_count("3/4")
    second_guest_waiting_room.wait_for_player_count("3/4")
    host_waiting_room.add_bots(1)
    
    host_waiting_room.wait_for_player_count("4/4")
    guest_waiting_room.wait_for_player_count("4/4")
    second_guest_waiting_room.wait_for_player_count("4/4")
    
    assert host_waiting_room.match_name() == match_name
    assert guest_waiting_room.match_name() == match_name
    assert second_guest_waiting_room.match_name() == match_name

    host_game_screen = host_waiting_room.start_game()
    guest_game_screen = ScreenPage(guest_waiting_room.page, guest_waiting_room.base_url)
    second_guest_game_screen = ScreenPage(
        second_guest_waiting_room.page, second_guest_waiting_room.base_url
    )

    guest_game_screen.assert_loaded()
    second_guest_game_screen.assert_loaded()

    for game_screen in (host_game_screen, guest_game_screen, second_guest_game_screen):
        game_screen.dismiss_tutorial_if_present()
        game_screen.dismiss_game_instructions_if_present()
        game_screen.assert_loaded()

    host_game_screen.wait_for_turn("blue")
    host_game_screen.assert_turn_is("blue")
    blue_soldier_position = host_game_screen.soldier_position(1)
    host_game_screen.enter_soldier(color="blue")
    host_game_screen.assert_soldier_visible(1)
    host_game_screen.assert_soldier_moved(1, from_position=blue_soldier_position)

    host_game_screen.wait_for_turn("red")
    red_soldier_position = guest_game_screen.soldier_position(5)
    guest_game_screen.move_piece(steps=2, color="red")
    guest_game_screen.assert_soldier_visible(5)
    guest_game_screen.assert_soldier_moved(5, from_position=red_soldier_position)

    host_game_screen.wait_for_turn("pink")
    pink_soldier_position = second_guest_game_screen.soldier_position(9)
    second_guest_game_screen.move_piece(steps=3, color="pink")
    second_guest_game_screen.assert_soldier_visible(9)
    second_guest_game_screen.assert_soldier_moved(9, from_position=pink_soldier_position)

    assert host_game_screen.current_turn_color() in {"red", "blue", "pink", "green"}