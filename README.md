# ParaBank Test Automation

## What's This?

This is a test automation framework for testing ParaBank banking app. It has both UI tests (using Playwright) and API tests (using requests library).

## Tech Stack

- Python 3.11+
- Playwright (for UI tests)
- Requests (for API tests)
- Pytest (test runner)
- pytest-ordering (test execution order)
- Allure (for reports)
- GitHub Actions (CI)
- autopep8 (for PEP8 styule-check)


## Installation Instructions

### Prerequisites
- Python 3.11 or higher
- Git

### Setup Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd parabank-qa-automation
```

2. **Create virtual environment:**
```bash
# Initialize virtual environment
python3 -m venv .venv

# Activate (Mac/Linux)
source .venv/bin/activate

# Activate (Windows)
.\.venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

**Note:** This installs all required packages including:
- `pytest` - Test framework
- `playwright` - Browser automation
- `pytest-playwright` - Playwright plugin for pytest
- `pytest-ordering` - Controls test execution order
- `allure-pytest` - Reporting

4. **Install Playwright browsers:**
```bash
playwright install --with-deps chromium
```

5. **Verify installation:**
```bash
pytest --version
playwright --version
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

## How to Run Tests

### UI Tests

**Run all UI tests (in correct order):**
```bash
pytest ui/ -v
```

**Test execution order:**
1. `test_register_new_user` - Creates user account (runs first)
2. `test_successful_login` - Tests valid login
3. `test_failed_login` - Tests invalid password

**Run specific UI test:**
```bash
pytest ui/test_login_ui.py -v
```

**Run with browser visible (headed mode):**
```bash
pytest ui/ -v --headed
```

**Run individual test cases:**
```bash
# TC_UI_01 - Successful login
pytest ui/test_login_ui.py::test_successful_login -v

# TC_UI_02 - Failed login
pytest ui/test_login_ui.py::test_failed_login -v

# Registration test
pytest ui/test_register_ui.py::test_register_new_user -v
```

### API Tests

**Run all API tests:**
```bash
pytest api/ -v
```

**Note:** API tests are currently skeleton files (empty). They will be implemented in future iterations.

### All Tests

**Run everything:**
```bash
pytest -v
```

## Test Reports

### HTML Reports

**Generate HTML report:**
```bash
pytest ui/ -v --html=reports/test-report.html --self-contained-html
```

### Allure Reports

**Generate and view Allure report:**
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## CI/CD Pipeline

### How the Pipeline Works

The project uses **GitHub Actions** for continuous integration:

**File:** `.github/workflows/ci.yml`

**Triggers:**
- Every push to `master` branch
- Every pull request to `master` branch

**Pipeline Steps:**
1. **Setup Environment**
   - Checkout code from repository
   - Set up Python 3.11
   - Install project dependencies from `requirements.txt`

2. **Install Browser**
   - Install Playwright Chromium browser with system dependencies

3. **Run Tests**
   - Execute UI tests: execute UI test (for now)
   - Tests run in headless mode (no visible browser)

4. **Results**
   - View test results in GitHub Actions logs
   - Green check = all tests passed
   - Red X = tests failed

### Viewing Pipeline Results

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click on latest workflow run
4. Expand **"Run UI tests"** to see detailed results
