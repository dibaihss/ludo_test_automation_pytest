import pytest

from pages.screen_page import ScreenPage


TURN_ACTIONS = {
    # "blue": {"action": "enter", "soldier_id": 1},
    "blue": {"action": "move", "soldier_id": 1, "steps": 4},
    "green": {"action": "enter", "soldier_id": 13},
    "red": {"action": "move", "soldier_id": 5, "steps": 2},
    "pink": {"action": "move", "soldier_id": 9, "steps": 3},
}


def _turn_plan(game_screens: list[ScreenPage], bot_count: int) -> dict[str, ScreenPage | None]:
    if len(game_screens) == 3 and bot_count == 1:
        return {
            "blue": game_screens[0],
            "green": game_screens[1],
            "red": game_screens[1],
            "pink": game_screens[2],
        }
    if len(game_screens) == 4 and bot_count == 0:
        return {
            "blue": game_screens[0],
            "green": game_screens[3],
            "red": game_screens[1],
            "pink": game_screens[2],
        }
    if len(game_screens) == 2 and bot_count == 2:
        return {
            "blue": game_screens[0],
            "green": None,
            "red": game_screens[1],
            "pink": None,
        }
    raise AssertionError(
        f"Unsupported turn plan for {len(game_screens)} human players and {bot_count} bots"
    )


def _play_assigned_turn(
    host_game_screen: ScreenPage,
    color: str,
    acting_screen: ScreenPage | None,
) -> None:
    host_game_screen.wait_for_turn(color)
    if acting_screen is None:
        host_game_screen.wait_for_turn_to_change_from(color)
        return

    action = TURN_ACTIONS[color]
    soldier_id = action["soldier_id"]
    if action["action"] == "enter":
        acting_screen.enter_soldier(color=color)
        acting_screen.assert_soldier_visible(soldier_id)
    else:
        acting_screen.move_piece(action["steps"], color=color)

    acting_screen.skip_turn()
    host_game_screen.wait_for_turn_to_change_from(color)


def _play_opening_round(
    host_game_screen: ScreenPage,
    assignments: dict[str, ScreenPage | None],
) -> None:
    acted_colors: set[str] = set()
    human_colors = {color for color, screen in assignments.items() if screen is not None}
    max_turns = len(assignments) * 3

    for _ in range(max_turns):
        current_color = host_game_screen.current_turn_color()
        acting_screen = assignments.get(current_color)
        if acting_screen is None:
            host_game_screen.wait_for_turn_to_change_from(current_color)
            continue

        if current_color in acted_colors:
            acting_screen.skip_turn()
            host_game_screen.wait_for_turn_to_change_from(current_color)
            continue

        _play_assigned_turn(host_game_screen, current_color, acting_screen)
        acted_colors.add(current_color)
        if acted_colors == human_colors:
            return

    raise AssertionError(
        f"Did not complete opening round for human colors: {sorted(human_colors - acted_colors)}"
    )


@pytest.mark.parametrize(
    ("online_players", "bot_count"),
    [
        pytest.param(2, 2, id="one-guest-join-and-play-round"),
        pytest.param(3, 1, id="two-guests-join-and-play-round"),
        pytest.param(4, 0, id="three-guests-join-and-play-round"),
    ],
    indirect=["online_players"],
)
def test_guest_players_can_create_join_and_start_match(
    online_players,
    bot_count: int,
):
    host_home_page = online_players[0]
    guest_home_pages = online_players[1:]
    host_match_list = host_home_page.open_multiplayer()
    host_waiting_room = host_match_list.create_match()
    match_name = host_waiting_room.match_name()

    guest_waiting_rooms = []
    for guest_home_page in guest_home_pages:
        guest_match_list = guest_home_page.open_multiplayer()
        guest_waiting_rooms.append(guest_match_list.join_match(match_name))

    expected_human_count = f"{len(online_players)}/4"
    host_waiting_room.wait_for_player_count(expected_human_count)
    for guest_waiting_room in guest_waiting_rooms:
        guest_waiting_room.wait_for_player_count(expected_human_count)

    host_waiting_room.add_bots(bot_count)
    host_waiting_room.wait_for_player_count("4/4")
    for guest_waiting_room in guest_waiting_rooms:
        guest_waiting_room.wait_for_player_count("4/4")

    assert host_waiting_room.match_name() == match_name
    for guest_waiting_room in guest_waiting_rooms:
        assert guest_waiting_room.match_name() == match_name

    host_game_screen = host_waiting_room.start_game()
    guest_game_screens = [
        ScreenPage(guest_waiting_room.page, guest_waiting_room.base_url)
        for guest_waiting_room in guest_waiting_rooms
    ]

    for game_screen in (host_game_screen, *guest_game_screens):
        game_screen.dismiss_tutorial_if_present()
        game_screen.dismiss_game_instructions_if_present()
        game_screen.assert_loaded()

    all_game_screens = [host_game_screen, *guest_game_screens]
    _play_opening_round(host_game_screen, _turn_plan(all_game_screens, bot_count))

    assert host_game_screen.current_turn_color() in {"red", "blue", "pink", "green"}