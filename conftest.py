import yaml
import pytest
import requests
from ui.pages import (LoginPage, AccountsOverviewPage,
                      AccountDetailsPage, TransferFundsPage)
from api.api_client import ParaBankAPIClient


@pytest.fixture(scope="session")
def settings():
    """Load settings from YAML file"""
    with open("config/settings.yaml") as f:
        # converts yaml file to python dictionary
        return yaml.safe_load(f)


@pytest.fixture
def login_page(page):
    """Fixture for LoginPage"""
    return LoginPage(page)



@pytest.fixture
def accounts_page(page):
    """Fixture for AccountsOverviewPage"""
    return AccountsOverviewPage(page)


@pytest.fixture
def account_details_page(page):
    """Fixture for AccountDetailsPage"""
    return AccountDetailsPage(page)


@pytest.fixture
def transfer_page(page):
    """Fixture for TransferFundsPage"""
    return TransferFundsPage(page)


@pytest.fixture
def config(settings):
    """Fixture to provide configuration settings for UI tests"""
    class Config:
        def __init__(self, settings):
            self.base_url = settings['ui_base_url']
            self.overview_url = settings['overview_url']
            self.username = settings['username']
            self.password = settings['password']
            self.invalid_password = settings['invalid_password']
            self.first_name = settings['first_name']

    return Config(settings)


@pytest.fixture(autouse=True)
def check_sut_health(request, config):
    """Automatically check if SUT login endpoint is healthy before running UI tests.
    
    Tests the actual login endpoint since that's where 5xx errors occur.
    Skips test if login returns 5xx or is unreachable.
    """
    # Only run health check for UI tests
    if "ui" not in str(request.fspath):
        return
    
    # Check login endpoint specifically (where the 500 errors happen)
    try:
        response = requests.post(
            f"{config.base_url}/login.htm",
            data={"username": config.username, "password": config.password},
            timeout=10,
            allow_redirects=False
        )
        
        # If login endpoint returns 5xx, skip the test
        if response.status_code >= 500:
            pytest.skip(f"Login endpoint down: HTTP {response.status_code}")
            
    except Exception as e:
        pytest.skip(f"Login endpoint unreachable: {e}")
# -------- API fixtures (data setup) --------

@pytest.fixture(scope="session")
def api_client(settings):
    """Fixture to provide API client instance"""
    return ParaBankAPIClient(settings["api_base_url"])

@pytest.fixture(scope="session")
def customer_id(settings) -> int:
    return int(settings["customer_id"])  # from config/settings.yaml


@pytest.fixture()
def valid_account_id(api_client: ParaBankAPIClient, customer_id: int) -> int:
    """Obtain a valid account id for the test customer (independent setup)."""
    resp = api_client.get_customer_accounts(customer_id)
    assert resp.status_code == 200, f"Precondition failed: accounts list status {resp.status_code}"
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0, "Precondition failed: no accounts returned for customer"
    first = data[0]
    assert "id" in first, "Precondition failed: account missing 'id'"
    return int(first["id"])
