import allure
from ui.pages import LoginPage


# TC_UI_03 - View Details of the First Account
@allure.feature("Accounts")
@allure.story("TC_UI_03")
@allure.title("View details of the first account")
@allure.severity(allure.severity_level.NORMAL)
def test_view_account_details(login_page: LoginPage, config):
    with allure.step("Navigate and login"):
        login_page.navigate(config.base_url)
        accounts_page = login_page.login(config.username, config.password)

    with allure.step("Verify Accounts Overview page"):
        accounts_page.verify_url(config.overview_url)
        accounts_page.verify_accounts_table_visible()

    with allure.step("Get first account number and open details"):
        account_number = accounts_page.get_first_account_number()
        account_details_page = accounts_page.open_first_account()

    with allure.step("Verify account details page"):
        account_details_page.verify_account_number(account_number)
        account_details_page.verify_balance_visible()
        account_details_page.verify_balance_format()
        account_details_page.verify_account_type_visible()
        account_details_page.verify_transactions_table_visible()
