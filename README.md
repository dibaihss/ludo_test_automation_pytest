# Strategic Ludo test automation

This project uses pytest and Playwright with the Page Object Model to automate the Strategic Ludo web app.

## Current coverage

- Entry page validation for the live login/landing screen.
- Home page validation after choosing `Play Offline`.
- Offline bot flow through the difficulty picker.
- Offline turn-cycle and piece-movement checks.
- Guest login on the online flow.
- Multiplayer match creation and joining with parameterized two-player and three-player scenarios.
- Multiplayer waiting-room flow with bot filling and game start.
- First shared multiplayer round validation for blue, red, and pink turns.

## Project structure

- `pages/` contains page objects for the entry page, home page, match list, waiting room, and game screen.
- `tests/` contains end-to-end tests.
- `conftest.py` provides browser fixtures and screenshot-on-failure support.
- `artifacts/screenshots/` stores failure screenshots.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Run tests

```powershell
pytest
```

Run a single file:

```powershell
pytest tests/test_offline_navigation.py
```

Run the online multiplayer file:

```powershell
pytest tests/online/test_multiplayer_create_join.py
```

Run only one parameterized multiplayer scenario:

```powershell
pytest tests/online/test_multiplayer_create_join.py -k one-guest-joins
pytest tests/online/test_multiplayer_create_join.py -k two-guests-join-and-play-round
```

Run headed mode:

```powershell
$env:HEADLESS = "false"
pytest tests/test_basic_gameplay_navigation.py
```

## Configuration

These environment variables are supported:

- `BASE_URL` defaults to `https://strategic.expo.app/`
- `BROWSER` defaults to `chromium`
- `HEADLESS` defaults to `true`
- `SLOW_MO` defaults to `0`
- `VIEWPORT_WIDTH` defaults to `1440`
- `VIEWPORT_HEIGHT` defaults to `1024`
- `SCREENSHOT_DIR` defaults to `artifacts/screenshots`

You can set them in a local `.env` file at the project root. Example:

```dotenv
BASE_URL=https://strategic.expo.app/
HEADLESS=false
SLOW_MO=1000
VIEWPORT_WIDTH=1440
VIEWPORT_HEIGHT=1024
```

Values from the shell still win over `.env` values if both are set.

For local development against the app running on port `8081`, a typical `.env` looks like this:

```dotenv
BASE_URL=http://localhost:8081/
HEADLESS=false
SLOW_MO=1000
VIEWPORT_WIDTH=1440
VIEWPORT_HEIGHT=1024
```

For a phone-sized viewport without full device emulation, set for example:

```dotenv
VIEWPORT_WIDTH=390
VIEWPORT_HEIGHT=844
```

`BASE_URL` must be a full URL such as `https://strategic.expo.app/` or `http://localhost:8081/`.

## Multiplayer Notes

- The online multiplayer tests use one shared browser instance with multiple isolated Playwright contexts, one per player.
- The `online_players` fixture is indirect and parameterized by player count inside the test file.
- The two built-in multiplayer scenarios are:
	- one guest joins and the host fills the room with two bots
	- two guests join, the host fills the room with one bot, and the test validates the first shared gameplay round
- The three-player gameplay assertions use the host screen as the reliable source of global turn progression, while the owning guest clients perform the red and pink actions.

## Adding coverage

Add new page objects under `pages/` and keep selectors inside those classes. Tests should call page-object methods and avoid direct locator usage.