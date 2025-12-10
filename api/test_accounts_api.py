import allure

class TestAccountsAPI:
    """Test class for Accounts API endpoints (validations using API wrapper)"""
    
    @allure.feature("API - Accounts")
    @allure.story("TC_API_01")
    @allure.title("Get accounts list for valid customer ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_customer_accounts_valid_id(self, api_client, customer_id):
        """TC_API_01: Get accounts list for valid customer ID"""

        with allure.step(f"Send GET request to /customers/{customer_id}/accounts"):
            response = api_client.get_customer_accounts(customer_id)

        with allure.step("Verify status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response body is a JSON list"):
            accounts = response.json()
            assert isinstance(accounts, list), "Expected response to be a JSON list"

        with allure.step("Verify accounts list is not empty"):
            assert accounts, "Accounts list should not be empty"

        with allure.step("Verify each account has required fields and balance is numeric"):
            for account in accounts:
                assert {"id", "type", "balance"} <= account.keys()
                assert isinstance(account["balance"], (int, float))

    @allure.feature("API - Accounts")
    @allure.story("TC_API_02")
    @allure.title("Get account details for a valid account ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_account_details_valid_id(self, api_client, valid_account_id):
        """TC_API_02: Get account details for a valid account ID"""

        with allure.step(f"Send GET request for account {valid_account_id}"):
            response = api_client.get_account_details(valid_account_id)

        with allure.step("Verify status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response body is a JSON object"):
            body = response.json()
            assert isinstance(body, dict),  "Expected response to be a JSON object"

        with allure.step("Verify account ID matches the requested ID"):
            assert int(body.get("id")) == int(valid_account_id)

        with allure.step("Verify balance field exists and is numeric"):
            assert "balance" in body, "Missing 'balance' field"
            assert isinstance(body["balance"], (int, float)), "Balance must be numeric"

        with allure.step("Validate key fields and types"):
            assert isinstance(body.get("customerId"), int)
            assert isinstance(body.get("type"), str)

    @allure.feature("API - Accounts")
    @allure.story("TC_API_03")
    @allure.title("Create new account via POST /createAccount")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_new_account(self, api_client, customer_id, valid_account_id, settings):
        """TC_API_03: Create new account via POST /createAccount"""
        with allure.step("Prepare account creation parameters"):
            new_account_type = settings["new_account_type"]
            from_account_id = valid_account_id
            allure.attach(f"Customer ID: {customer_id}\nAccount Type: {new_account_type}\nFrom Account: {from_account_id}",
                         name="Request Parameters", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Send POST request to /createAccount"):
            response = api_client.create_account(customer_id, new_account_type, from_account_id)

        with allure.step("Verify status code is 200 or 201"):
            assert response.status_code in (200, 201), f"Unexpected status code: {response.status_code}"

        with allure.step("Verify response body is a JSON object with new account id"):
            body = response.json()
            assert isinstance(body, dict), "Expected response to be a JSON object"
            assert "id" in body

        with allure.step("Verify the created account can be retrieved"):
            created_id = int(body["id"])
            # compare the Created account with the when created from the POST call
            allure.attach(f"Created Account ID: {created_id}", 
                         name="New Account", attachment_type=allure.attachment_type.TEXT)
            details = api_client.get_account_details(created_id)
            assert details.status_code == 200
            # Ensure created account is exist
            details_body = details.json()
            assert isinstance(details_body, dict), "Expected account details to be a JSON object"
            assert int(details_body.get("id")) == created_id

    @allure.feature("API - Accounts")
    @allure.story("TC_API_04")
    @allure.title("Request account details with invalid account ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_account_details_invalid_id(self, api_client, settings):
        """TC_API_04: Request account details with invalid account ID"""

        with allure.step("Get invalid account ID from settings"):
            invalid_id = int(settings["invalid_account_id"])
            # to validate if the fetched ID is indeed invalid --> should be 999999999 from the seetings file
            allure.attach(f"Invalid Account ID: {invalid_id}", 
                         name="Test Data", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Send GET request with invalid account ID {invalid_id}"):
            response = api_client.get_account_details(invalid_id)

        with allure.step("Verify status code is 4xx"):
            assert 400 <= response.status_code < 500, "Expected 4xx status code"

        with allure.step("Verify error message/body is present"):
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                body = response.json()
                assert body, "Expected non-empty JSON error body"
            else:
                assert response.text, "Expected non-empty error message in response body"
