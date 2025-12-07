"""POM package for UI automation"""

from .login_page import LoginPage
from .register_page import RegisterPage
from .accounts_page import AccountsOverviewPage
from .account_details_page import AccountDetailsPage
from .transfer_page import TransferFundsPage

__all__ = [
    'LoginPage',
    'RegisterPage',
    'AccountsOverviewPage',
    'AccountDetailsPage',
    'TransferFundsPage',
]
