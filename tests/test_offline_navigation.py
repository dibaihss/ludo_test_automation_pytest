from pages.entry_page import EntryPage
from pages.home_page import HomePage
from pages.screen_page import ScreenPage


def test_play_offline_to_game_screen(page, settings):
    entry_page = EntryPage(page, settings.base_url)
    home_page = HomePage(page, settings.base_url)
    screen_page = ScreenPage(page, settings.base_url)

    entry_page.open()
    entry_page.assert_loaded()

    entry_page.start_offline()
    home_page.assert_loaded()

    home_page.start_offline_vs_bot(difficulty="Easy")
    screen_page.assert_loaded()


def test_home_page_opens_offline_options(page, settings):
    entry_page = EntryPage(page, settings.base_url)
    home_page = HomePage(page, settings.base_url)

    entry_page.open()
    entry_page.start_offline()

    home_page.assert_loaded()
    home_page.open_offline_options()