import requests

class ParaBankAPIClient:
    """API client wrapper for ParaBank REST API calls"""

    def __init__(self, api_base_url):
        """Initialize the API client with base URL"""
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
    
    def get_customer_accounts(self, customer_id):
        return self.session.get(f"{self.api_base_url}/customers/{customer_id}/accounts")

    def get_account_details(self, account_id):
        return self.session.get(f"{self.api_base_url}/accounts/{account_id}")

    def create_account(self, customer_id, account_type, from_account_id):
        return self.session.post(
        f"{self.api_base_url}/createAccount",
        params={
            "customerId": customer_id,
            "newAccountType": account_type,
            "fromAccountId": from_account_id
        }
    )    
    def transfer_funds(self, amount, from_account, to_account):
        return self.session.post(
        f"{self.api_base_url}/transfer",
        params={
            "amount": amount,
            "fromAccountId": from_account,
            "toAccountId": to_account
        }
    )
