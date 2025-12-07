from ui.pages import LoginPage


# TC_UI_03 - View Details of the First Account
def test_view_account_details(login_page: LoginPage, config):
    # Navigate and login
    login_page.navigate(config.base_url)
    accounts_page = login_page.login(config.username, config.password)

    # Verify Accounts Overview page
    accounts_page.verify_url(config.overview_url)
    accounts_page.verify_accounts_table_visible()

    # Get first account number and open details
    account_number = accounts_page.get_first_account_number()
    account_details_page = accounts_page.open_first_account()

    # Verify account details
    account_details_page.verify_account_number(account_number)
    account_details_page.verify_balance_visible()
    account_details_page.verify_balance_format()
    account_details_page.verify_account_type_visible()
    account_details_page.verify_transactions_table_visible()
