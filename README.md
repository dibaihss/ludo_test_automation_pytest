# Strategic Ludo test automation

This project uses pytest and Playwright with the Page Object Model to automate the Strategic Ludo web app at https://strategic.expo.app/.

## Current coverage

- Entry page validation for the live login/landing screen.
- Home page validation after choosing `Play Offline`.
- Offline bot flow through the difficulty picker.
- Game screen validation and tutorial dismissal.

## Project structure

- `pages/` contains page objects for the entry page, home page, and game screen.
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

You can set them in a local `.env` file at the project root. Example:

```dotenv
BASE_URL=https://strategic.expo.app/
HEADLESS=false
SLOW_MO=1000
VIEWPORT_WIDTH=1440
VIEWPORT_HEIGHT=1024
```

Values from the shell still win over `.env` values if both are set.

## Adding coverage

Add new page objects under `pages/` and keep selectors inside those classes. Tests should call page-object methods and avoid direct locator usage.