# ParaBank Assessment - Task Requirements & BDD Scenarios


## Framework Stack
- **Python** - Programming language
- **Playwright (UI)** - Browser automation for UI testing
- **Requests (API)** - HTTP library for API testing
- **Pytest** - Test runner framework

- **Allure reporting** - Test reporting and documentation
- **CI** - GitHub Actions continuous integration


---

## Table of Contents
- [UI Automation Requirements](#ui-automation-requirements)
- [API Automation Requirements](#api-automation-requirements)
- [Technical Requirements](#technical-requirements)
- [BDD Scenarios - UI](#bdd-scenarios---ui)
- [BDD Scenarios - API](#bdd-scenarios---api)

---

## UI Automation Requirements

Implement at least **4 UI tests** using Playwright following the **Page Object Model (POM)** pattern.

### UI Test 1 — Successful Login

**Test Steps:**
1. Open the ParaBank homepage
2. Login using valid credentials (stored in config)

**Validations:**
- The welcome message with customer name is displayed
- Account list is displayed

---

### UI Test 2 — Failed Login

**Test Steps:**
1. Open the ParaBank homepage
2. Use invalid password
3. Attempt to login

**Validations:**
- Error message is displayed
- Accounts page is not accessible

---

### UI Test 3 — View Account Details

**Test Steps:**
1. Login with valid credentials
2. Open the first available account from the account list

**Validations:**
- Account number is displayed
- Balance is displayed
- Account type is displayed
- Transactions table is displayed

---

### UI Test 4 — Transfer Funds Between Own Accounts

**Test Steps:**
1. Login with valid credentials
2. Navigate to "Transfer Funds"

3. Transfer an amount (e.g., 10 USD) from one account to another


**Validations:**
- Success message is displayed
- Balances changed correctly (before → after)


**Note:** UI code should follow **Page Object Model (POM)** pattern.

---

## API Automation Requirements

Implement at least **4 API tests** using the `requests` library. API tests should be independent, using **pytest fixtures** for data setup.

### API Test 1 — Get List of Accounts for a Customer

**Test Steps:**
1. Call `/accounts?customerId={id}` or similar endpoint

**Validations:**
- Status code 200
- Non-empty list of accounts
- Each account has: `id`, `type`, `balance`

---

### API Test 2 — Get Account Details

**Test Steps:**
1. Use accountId from the previous test
2. Call `/accounts/{id}`

**Validations:**
- Status code 200
- Correct account ID
- Balance field is present
- Correct data types

---

### API Test 3 — Create New Resource (POST)

**Test Steps:**
1. Send POST request to create a new resource (account, payee, or transfer)
   - Depends on what API supports

**Validations:**
- Status code 200/201
- Correct fields in response

---

### API Test 4 — Negative Test

**Test Steps:**
1. Call an endpoint with invalid accountId or missing parameters

**Validations:**
- Correct 4xx error status code
- Error message in response

---

## Technical Requirements

### General Validation Requirements
- No hardcoded credentials inside test logic
- Use fixtures for:
  - Base URL
  - Valid user credentials
  - Reusable API clients
- Tests must be independent (no dependency on other test execution order)

### Allure Reporting Requirements
**Expected Behavior:**
- Each test must include Allure metadata:
  - Features
  - Stories
  - Steps (using `allure.step`)
- For API tests:
  - Attach response body when validating
- For UI tests:
  - Optionally attach screenshots or failure evidence

### Teardown / Data Independence
- API tests must not rely on UI state
- UI tests must not rely on API tests
- No destructive changes that break other tests

---

## BDD Scenarios - UI

### Feature: Customer Login

Feature: Customer Login
  As a ParaBank customer I want to login to my account
AC1
  @ui @login @positive
  Scenario: Successful login with valid credentials
  Given the ParaBank login page is available
    When I enter a valid username
    And I enter a valid password
    And I click the Login button
    Then I should see the Accounts Overview page
    And I should see a welcome message with my name
    And I should see a list of my accounts
AC2
  @ui @login @negative
  Scenario: Failed login with invalid password
  Given the ParaBank login page is available
    When I enter a valid username
    And I enter an invalid password
    And I click the Login button
    Then I should see Error message displayed
    And Accounts page is not accessible

---

### Feature: View Account Details

Feature: View account details
  As a logged-in customer
  I want to view the details of my accounts
  So that I can see balances and transactions
AC3
  @ui @accounts @details
  Scenario: View details of the first account
  Given I am logged in with valid credentials
    And I am on the Accounts Overview page
    When I open the first account in the account list
    Then I should see the Account Details page
    And I should see the correct account number
    And I should see the current account balance
    And I should see the account type
    And I should see a transactions table for this account

---

### Feature: Transfer Funds Between Own Accounts

Feature: Transfer funds between own accounts
  As a logged-in customer
  I want to transfer money between my own accounts
  So that I can manage my balances
AC4
  @ui @transfer @positive
  Scenario: Successful transfer between two accounts
  Given I am logged in with valid credentials
    And I have at least two accounts
    And I am on the Accounts Overview page
    And I increased by 10e the current balance of the source account
    When I navigate to the Transfer Funds page
    And I select the source-to-target account in the From Account field
    And I enter a transfer amount of 10
    And I submit the transfer
    Then I should see a successful transfer confirmation message
    And the source account balance should be reduced by 10
    And the target account balance should be increased by 10

---

## BDD Scenarios - API

### Feature: Accounts API – List & Details

Feature: As an API backend tester, I want to retrieve account information
  So that I can validate account data for a customer
AC5
  @api @accounts_listing
  Scenario: Get list of accounts for a valid customer
  Given the Accounts API URL is available
    And I have a valid customer ID
    When I request the list of accounts for this customer
    Then the response status code should be 200
    And the response should contain a non-empty list of accounts
    And each account should have an id field
    And each account should have a type field
    And each account should have a balance field
AC6
  @api @accounts-details
  Scenario: Get account details for a valid account
  Given the Accounts API URL is available
    And I have a valid account ID for an existing account
    When I request the details for this account
    Then the response status code should be 200
    And the response should contain the same account ID
    And the response should contain a balance field
    And all fields should have the expected data types

---

### Feature: Accounts API – Create Resource and Negative Cases

Feature: Accounts API - creating resources and negative responses
  As an API consumer
  I want to create new banking resources
  And see appropriate error handling
  So that I can validate system behavior
AC7
  @api @create @positive
  Scenario: Create a new resource via POST (e.g. transfer or account)
  Given the Accounts API URL is available
    And I have a valid request [body] for creating a new resource
    When I send a POST request to the endpoint URL
    Then the response status code should be 201(created)
    And the response should contain the key fields for the created resource
    And the response data should match the request parameters where applicable
AC8
  @api @negative
  Scenario: Request account details with an invalid account ID
  Given the Accounts API URL is available
    And I have a nn-existing account ID
    When I request the details for this invalid account
    Then the response status code should be a 4xx error
    And the response should contain an error message

---

## Notes for Implementation

### Test Organization
- Organize tests by feature/module
- Use descriptive test names that explain the scenario
- Keep test files focused and manageable in size

### Data Management
- Store test data in separate files or fixtures
- Use `.env` file for environment-specific configurations
- Never commit sensitive credentials to version control

### Reporting Best Practices
- Add meaningful step descriptions
- Attach relevant artifacts (screenshots, API responses)
- Use appropriate severity levels for tests
- Group related tests under the same feature/epic

### Code Quality
- Follow PEP 8 style guidelines
- Add docstrings to test functions
- Use meaningful variable and function names
- Keep functions small and focused on a single responsibility
