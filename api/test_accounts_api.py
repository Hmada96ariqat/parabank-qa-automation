class TestAccountsAPI:
    """Test class for Accounts API endpoints (validations using API wrapper)"""
    
    def test_get_customer_accounts_valid_id(self, api_client, customer_id):
        """TC_API_01: Get accounts list for valid customer ID"""

        # Step 1: Send GET request to /customers/{customerId}/accounts
        response = api_client.get_customer_accounts(customer_id)

        # Step 2: Verify status code is 200
        assert response.status_code == 200

        # Step 3: Verify response body is a JSON list
        accounts = response.json()
        assert isinstance(accounts, list), "Expected response to be a JSON list"

        # Step 4: Verify accounts list is not empty
        assert accounts, "Accounts list should not be empty"

        # Step 5: Verify each account has required fields and balance is numeric
        for account in accounts:
            assert {"id", "type", "balance"} <= account.keys()
            assert isinstance(account["balance"], (int, float))

    def test_get_account_details_valid_id(self, api_client, valid_account_id):
        """TC_API_02: Get account details for a valid account ID"""

        # Step 1: Send GET request for account details
        response = api_client.get_account_details(valid_account_id)

        # Step 2: Verify status code is 200
        assert response.status_code == 200

        # Step 3: Verify response body is a JSON object
        body = response.json()
        assert isinstance(body, dict),  "Expected response to be a JSON object"

        # Step 4: Verify account ID matches the requested ID
        assert int(body.get("id")) == int(valid_account_id)

        # Step 5: Verify balance field exists and is numeric
        assert "balance" in body, "Missing 'balance' field"
        assert isinstance(body["balance"], (int, float)), "Balance must be numeric"

        # Step 6: Validate key fields and types
        assert isinstance(body.get("customerId"), int)
        assert isinstance(body.get("type"), str)

    def test_create_new_account(self, api_client, customer_id, valid_account_id, settings):
        """TC_API_03: Create new account via POST /createAccount"""
        # Use a test account type from settings
        new_account_type = settings["new_account_type"]
        from_account_id = valid_account_id

        # Step 1: Send POST request to /createAccount
        response = api_client.create_account(customer_id, new_account_type, from_account_id)

        # Step 2: Verify status code is 200 or 201
        assert response.status_code in (200, 201), f"Unexpected status code: {response.status_code}"

        # Step 3: Verify response body is a JSON object with new account id
        body = response.json()
        assert isinstance(body, dict), "Expected response to be a JSON object"
        assert "id" in body

        # Step 4: Verify the created account can be retrieved
        created_id = int(body["id"])
        details = api_client.get_account_details(created_id)
        assert details.status_code == 200
        # Ensure created account is exist
        details_body = details.json()
        assert isinstance(details_body, dict), "Expected account details to be a JSON object"
        assert int(details_body.get("id")) == created_id

    def test_get_account_details_invalid_id(self, api_client, settings):
        """TC_API_04: Request account details with invalid account ID"""

        invalid_id = int(settings["invalid_account_id"])

        # Step 1: Send GET request with invalid account ID
        response = api_client.get_account_details(invalid_id)

        # Step 2: Verify status code is 4xx
        assert 400 <= response.status_code < 500, "Expected 4xx status code"

        # Step 3: Verify error message/body is present
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            body = response.json()
            assert body, "Expected non-empty JSON error body"
        else:
            assert response.text, "Expected non-empty error message in response body"
