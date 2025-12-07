from ui.pages import LoginPage
from helpers.convert_currency import to_amount


# TC_UI_04 - Transfer Funds Between Two Own Accounts
def test_transfer_funds(login_page: LoginPage, config):
    transfer_amount = 10

    # Navigate and login
    login_page.navigate(config.base_url)
    accounts_page = login_page.login(config.username, config.password)

    # Verify Accounts Overview page
    accounts_page.verify_url(config.overview_url)
    accounts_page.verify_accounts_table_visible()

    # Get account numbers and balances before transfer
    source_account = accounts_page.get_first_account_number()
    source_balance_before = accounts_page.get_first_account_balance()
    target_account = accounts_page.get_second_account_number()
    target_balance_before = accounts_page.get_second_account_balance()

    # Navigate to Transfer Funds page
    transfer_page = accounts_page.navigate_to_transfer_funds()

    # Perform transfer
    transfer_page.transfer(transfer_amount, source_account, target_account)

    # Verify transfer completion
    transfer_page.verify_transfer_complete()

    # Return to Accounts Overview to verify balances
    accounts_page.navigate(config.overview_url)
    accounts_page.verify_accounts_table_visible()

    # Get updated balances
    source_balance_after = accounts_page.get_first_account_balance()
    target_balance_after = accounts_page.get_second_account_balance()

    # Convert balances to float for comparison
    source_before = to_amount(source_balance_before)
    source_after = to_amount(source_balance_after)
    target_before = to_amount(target_balance_before)
    target_after = to_amount(target_balance_after)

    # Verify balance changes
    assert source_after == source_before - transfer_amount, (
        f"Source balance should be "
        f"{source_before - transfer_amount}, but got {source_after}")
    assert target_after == target_before + transfer_amount, (
        f"Target balance should be "
        f"{target_before + transfer_amount}, but got {target_after}")
