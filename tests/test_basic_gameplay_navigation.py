def test_can_skip_tutorial_on_game_screen(offline_game_screen):
    offline_game_screen.assert_tutorial_visible()
    offline_game_screen.skip_tutorial()
    offline_game_screen.assert_tutorial_dismissed()
