from pages.screen_page import ScreenPage


def test_guest_player_can_create_and_second_guest_can_join(two_online_players):
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