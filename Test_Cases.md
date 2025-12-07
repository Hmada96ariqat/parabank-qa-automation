# Test Cases

## UI Test Cases

### TC_UI_01 – Successful Login with Valid Credentials (Related-to-AC1)

**Objective**  
Verify that a ParaBank customer can log in with valid credentials and see the Accounts Overview page.

**Preconditions**
1. Existing cutomer with username and password.

**Test Data** <GET THEM FROM THE SETTINGS.YAML>
- Username: <valid_username> 
- Password: <valid_password>

**Steps**
1. Navigate to https://parabank.parasoft.com/parabank.
2. Verify that the login form is displayed.
3. Enter a valid username in the Username field.
4. Enter a valid password in the Password field.
5. Click the Login button.

**Expected Result**
1. User is redirected to the Accounts Overview page.
2. A welcome message is displayed containing the customer’s name.
3. A list of accounts is visible (accounts table or links).

---

### TC_UI_02 – Failed Login with Invalid Password (Related-to-AC2) FAILED

**Objective**  
Verify that login fails when the user enters a valid username but an invalid password.

**Preconditions**
1. The user is on the login page.

**Test Data**
- Username: <valid_username>
- Password: <invalid_password> (use WrongPass123)

**Steps**
1. Navigate to https://parabank.parasoft.com/parabank.
2. Verify that the login form is displayed.
3. Enter a valid username in the Username field.
4. Enter an invalid password in the Password field.
5. Click the Login button.

**Expected Result**
1. User remains on the login page (no navigation to Accounts Overview).
2. An error message is displayed (e.g. “The username and password could not be verified”).
3. The Accounts Overview page and account list are not visible.

**Actual Result**
- the website log me in no matter if the creds were wrong

---

### TC_UI_03 – View Details of the First Account (Related-to-AC3)

**Objective**  
Verify that a logged-in customer can open the first account from the account list and view its details and transactions.

**Preconditions**
1. User has at least one active account.
2. User can successfully log in.

**Test Data**
- Valid username/password for a customer with accounts.

**Steps**
1. Log in to ParaBank with valid credentials.
2. Confirm that the Accounts Overview page is displayed.
3. Identify the first account in the accounts list.
4. Click the numbe(link) of the first account.

**Expected Result**
1. Account Details page is displayed.
2. The account number matches the selected account.
3. The current balance is shown and is a valid numeric value.
4. The account type is displayed.
5. A transactions table is visible.

---

### TC_UI_04 – Transfer Funds Between Two Own Accounts (Related-to-AC4)

**Objective**  
Verify that a logged-in customer can transfer funds between two owned accounts and that balances update correctly.

**Preconditions**
1. Existing user has at least two accounts (source and target).
2. User can log in successfully.

**Test Data**
- Valid username/password.
- Transfer amount: 10.

**Steps**
1. Log in to ParaBank with valid credentials.
2. From the Accounts Overview page note the current balance of source and target accounts.
3. Navigate to the Transfer Funds page.
5. Select the source account in the From Account# dropdown.
6. Select the target account in the To Account# dropdown.
7. Enter amount 10 in the Amount field.
8. Click the Transfer button.
9. Return to Accounts Overview and refresh balances.

**Expected Result**
1. A successful transfer confirmation message is displayed.
2. Source account balance =  - 10.
3. Target account balance =  + 10.

---

## API Test Cases

### TC_API_01 – Get Accounts List for Valid Customer (Related-to-AC5)

**Objective**  
Verify that the Accounts API returns a non-empty list of accounts for a valid customer ID.

**Preconditions**
1. API base URL is reachable: /parabank/services/bank.
2. A valid customerId exists (e.g. 12212 from demo data).

**Endpoint**
GET /customers/{customerId}/accounts

**Test Data**
- customerId = 12212 (example demo customer).

**Steps**
1. Send a GET request to /customers/{customerId}/accounts with a valid customerId.
2. Capture the HTTP response status code and body.

**Expected Result**
1. Status code is 200.
2. Response body is a JSON array (list) of accounts.
3. The list is not empty (length ≥ 1).
4. For each account object:
   - id field is present.
   - type field is present.
   - balance field is present and numeric.

---

### TC_API_02 – Get Account Details for Valid Account

Related AC: AC6 – Get account details for a valid account

**Objective**  
Verify that the Accounts API returns correct account details when queried with a valid account ID.

**Preconditions**
1. Test customer has at least one active account.
2. A valid accountId is obtained from TC_API_01 response.

**Endpoint**
GET /accounts/{accountId}

**Test Data**
- accountId = <valid account id from TC_API_01>

**Steps**
1. Send a GET request to /accounts/{accountId} with a valid accountId.
2. Capture response status code and body.

**Expected Result**
1. Status code is 200.
2. Response body is a JSON object representing the account.
3. Field id equals the requested accountId.
4. balance field exists and is numeric.
5. Other key fields (e.g. customerId, type) exist and have appropriate data types (int/string).

---

### TC_API_03 – Create New Resource via POST (Account or Transfer)

Related AC: AC7 – Create a new resource via POST

(Example below uses POST /createAccount; you can adapt to /transfer if you prefer.)

**Objective**  
Verify that the API can create a new account for a valid customer and returns expected fields.

**Preconditions**
1. API base URL is available.
2. Valid customerId and fromAccountId exist.

**Endpoint**
POST /createAccount

**Test Data**
- customerId = 12212 (example)
- newAccountType = 1 (e.g. SAVINGS)
- fromAccountId = <existing account ID>

**Steps**
1. Send a POST request to /createAccount with query parameters or form data as required: customerId, newAccountType, fromAccountId.
2. Capture the response status code and body.

**Expected Result**
1. Status code is 200 or 201 (created) depending on API implementation.
2. Response contains key fields for the created resource (e.g. new accountId or confirmation object).
3. Where applicable, response fields (e.g. customerId, newAccountType) match the request parameters.
4. No error message or fault is returned.

---

### TC_API_04 – Request Account Details with Invalid Account ID

Related AC: AC8 – Request account details with an invalid account ID

**Objective**  
Verify that the API returns an appropriate 4xx error when an invalid or non-existing account ID is used.

**Preconditions**
- API base URL is available.

**Endpoint**
GET /accounts/{accountId}

**Test Data**
- accountId = 999999999 (or another definitely non-existing ID).

**Steps**
1. Send a GET request to /accounts/{accountId} with the invalid ID.
2. Capture response status code and body.

**Expected Result**
1. Status code is a 4xx (e.g. 400 or 404 depending on server behavior).
2. Response body contains an error message or error structure indicating invalid or unknown account.
3. No valid account data is returned.
