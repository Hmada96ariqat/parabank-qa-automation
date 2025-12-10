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
    """Automatically check if SUT is accessible and login works before running UI tests.    
    Skips test if either check fails.
    """
    # Only run health check for UI tests
    if "ui" not in str(request.fspath):
        return
    
    try:
        # Check 1: Verify ParaBank site is accessible
        site_response = requests.get(
            config.base_url,
            timeout=10
        )
        
        if site_response.status_code >= 500:
            pytest.skip(f"ParaBank site down: HTTP {site_response.status_code}")
        
        # Check 2: Verify login endpoint accepts credentials
        login_response = requests.get(
            f"{config.base_url}/services/bank/login/{config.username}/{config.password}",
            timeout=10
        )
        
        # Skip if login API returns error
        if login_response.status_code >= 400:
            pytest.skip(f"Login validation failed: HTTP {login_response.status_code} - credentials may be invalid or DB unavailable")
            
    except Exception as e:
        pytest.skip(f"ParaBank unreachable: {e}")
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
