# ParaBank Test Plan

## 1. Introduction / Purpose

This test plan describes the testing approach for validating ParaBank's customer login, account overview, fund transfer, and account API functionalities. Both UI tests (Playwright) and API tests (Python requests) are included.

---

## 2. Test Scope

### In-Scope

- UI login validation
- Viewing accounts and account details
- Transferring funds between customer-owned accounts
- Validating account data via REST API
- Negative API tests (invalid account ID)

### Out-of-Scope

- Performance testing
- Security or penetration testing
- Browser compatibility testing
- Mobile testing
- Backend database validation

---

## 3. Test Approach

### UI Testing (Playwright/Python)

- Validate login behavior
- Validate post-login navigation
- Validate account overview and account details
- Validate transfer funds workflow

### API Testing

- REST API test using Python's requests lib
- Validate status codes, response structure, and key fields
- Positive and negative API scenarios

---

## 4. Test Environment

**SUT:**
- ParaBank demo environment: https://parabank.parasoft.com/parabank

**Testing Tools:**
-  Python 3.14.0
- Playwright
- pytest test runner
- Python requests library
- Allure for reporting

**Browser:**
- Chrome

---

## 5. Test Data

Test data is stored in `config/settings.yaml`:

- UI Base URL
- API Base URL
- Valid username & password
- User registration information

---

## 6. Risks 

- Demo environment may be unstable or slow
    note: (I will use longer wait than expected)
- API responses may vary unexpectedly
- ParaBank is accepting invalid credentials (bug in AC2)
- Demo site may reset user data periodically
    note: (I created a user registration test to avoid login crashes)

---

## 7. Test Cases Summary

| ID    | Title     |    Type    |  Status   |
|---|---|---|---|
| TC_UI_01  | Successful Login | UI | ✅ Passed |
| TC_UI_02 | Failed Login with Invalid Password | UI | ⚠️ Failed (System allows invalid login — defect) |
| TC_UI_03 | View Account Details | UI | ⏳ Pending execution |
| TC_UI_04 | Transfer Funds | UI | ⏳ Pending execution |
| TC_API_01 | Get Accounts List | API | ⏳ Pending execution |
| TC_API_02 | Get Account Details | API | ⏳ Pending execution |
| TC_API_03 | Create Resource via POST | API | ⏳ Pending execution |
| TC_API_04 | Invalid Account ID | API | ⏳ Pending execution |

---

## 8. Known Issues

**Issue #1: Invalid Login Credentials Accepted**
- **Test Case:** TC_UI_02
- **Severity:** High
- **Description:** The system allows login with invalid password
- **Expected:** Error message with "Invalid creds" messeage and remain on login page
- **Actual:** User is logged in successfully

---

## 9. Test Deliverables

- Test plan document (this file)
- Test cases (`Test_Cases.md`)
- BDD scenarios (for requirement anakysis)
- Test scripts (Python + Playwright)
- Test execution results
- Allure test reports
- GitHub CI pipeline

---

## 11. Entry & Exit Criteria

### Entry Criteria

- Test environment is accessible
- Test data is prepared in config files
- All dependencies are installed and inside the requirement.txt file

### Exit Criteria

- All planned test cases are executed
- Critical defects are reported
- Test results are documented
- Test reports are generated

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-06  
**Author:** Ahmad Areiqat
