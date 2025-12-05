# Sol-Ark Test Assessment

## What's This?

This is a test automation framework for testing ParaBank banking app. It has both UI tests (using Playwright) and API tests (using requests library).

## Tech Stack

- Python
- Playwright (for UI tests)
- Requests (for API tests)
- Pytest (test runner)
- Allure (for reports)

## Setup (on Mac environemtn)

1. Create virtual environment:
```bash
#initilization
python3 -m venv .venv
#to activate (Mac)
source .venv/bin/activate
#To activate (Windows)
.\.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

## Project Structure

```
├── api/                    # API tests
├── ui/                     # UI tests
│   └── pages/             # Page objects
├── config/                # Config files
├── conftest.py           # Pytest fixtures
└── pytest.ini            # Pytest config
```

## Running Tests

Run all tests:
```bash
pytest
```

Run only UI tests:
```bash
pytest ui/
```

Run only API tests:
```bash
pytest api/
```

## Allure Reports

Generate and view report:
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```
