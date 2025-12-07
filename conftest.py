import yaml
import pytest
from ui.pages import (LoginPage, RegisterPage, AccountsOverviewPage,
                      AccountDetailsPage, TransferFundsPage)


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
def register_page(page):
    """Fixture for RegisterPage"""
    return RegisterPage(page)


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
    """Fixture to provide configuration settings"""
    class Config:
        def __init__(self, settings):
            self.base_url = settings['ui_base_url']
            self.overview_url = settings['overview_url']
            self.username = settings['username']
            self.password = settings['password']
            self.invalid_password = settings['invalid_password']
            self.first_name = settings['first_name']
            self.last_name = settings['last_name']
            self.street = settings['street']
            self.city = settings['city']
            self.state = settings['state']
            self.zip_code = settings['zip_code']
            self.phone = settings['phone']
            self.ssn = settings['ssn']

    return Config(settings)
