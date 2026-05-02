import pytest
from playwright.sync_api import Page

from config import Settings
from pages.entry_page import EntryPage
from pages.home_page import HomePage


@pytest.fixture()
def play_online_mode(page: Page, settings: Settings) -> EntryPage:
    entry_page = EntryPage(page, settings.base_url)
    entry_page.open()
    entry_page.assert_loaded()

    return entry_page

@pytest.mark.parametrize("username", [
    "standard_user",
    "problem_user",
])
def test_login_as_guest(play_online_mode, username: str):
    home_page = HomePage(play_online_mode.page, play_online_mode.base_url)
    
    play_online_mode.login_as_guest()
    play_online_mode.enter_guest_username(username)
    play_online_mode.confirm_guest_username()
    
    home_page.assert_loaded()