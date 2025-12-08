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

**Run all UI tests (recommended):**
```bash
pytest ui/ -v
```

**Test execution order:**
1. `test_register_new_user` - Registers/ensures the test user exists (runs first)
2. `test_successful_login` (TC_UI_01) - Successful login with valid credentials
3. `test_failed_login` (TC_UI_02) - Failed login with invalid password
4. `test_view_account_details` (TC_UI_03) - View details of the first account
5. `test_transfer_funds` (TC_UI_04) - Transfer funds between two own accounts

**Run specific UI test file:**
```bash
pytest ui/test_login_ui.py -v
pytest ui/test_account_details_ui.py -v
pytest ui/test_transfer_ui.py -v
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

# TC_UI_03 - View account details
pytest ui/test_account_details_ui.py::test_view_account_details -v

# TC_UI_04 - Transfer funds between two own accounts
pytest ui/test_transfer_ui.py::test_transfer_funds -v

# Registration test (prerequisite for login & other flows)
pytest ui/test_register_ui.py::test_register_new_user -v
```

### API Tests

**Run all API tests:**
```bash
pytest api/ -v
```

**Implemented coverage**
- `TC_API_01` – `GET /customers/{customerId}/accounts` returns a non-empty list of accounts with required fields (`id`, `type`, `balance`).
- `TC_API_02` – `GET /accounts/{accountId}` returns a valid account object with matching `id`, numeric `balance`, and correct `customerId`/`type` types.
- `TC_API_03` – `POST /createAccount` creates a new account (using `customerId`, `newAccountType`, `fromAccountId`) and verifies it can be retrieved again.
- `TC_API_04` – `GET /accounts/{invalidId}` uses an invalid account id and asserts a 4xx error with an error payload or message.

**API client implementation**
- File: `api/api_client.py`
- Class: `ParaBankAPIClient`
- Loads `api_base_url` from `config/settings.yaml` by default.
- Wraps the ParaBank REST endpoints:
  - `get_customer_accounts(customer_id)` → `GET /customers/{customerId}/accounts`
  - `get_account_details(account_id)` → `GET /accounts/{accountId}`
  - `create_account(customer_id, new_account_type, from_account_id)` → `POST /createAccount`
  - `transfer_funds(amount, from_account_id, to_account_id)` → `POST /transfer`

**API test configuration**
- File: `config/settings.yaml`
- Important keys for API tests:
  - `api_base_url` – base URL for the  API endpoints
  - `customer_id` – existing customer id used for happy‑path scenarios
  - `invalid_account_id` – non‑existent account id used for negative scenarios


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
   - Tests run in headless mode (no visible browser) unless otherwise use --headed parameter

4. **Results**
   - View test results in GitHub Actions logs


### Viewing Pipeline Results

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click on latest workflow run
