import allure
from ui.pages import LoginPage, AccountsOverviewPage


# TC_UI_01 - Successful Login with Valid Credentials
@allure.feature("Login")
@allure.story("TC_UI_01")
@allure.title("Successful login with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(login_page: LoginPage, config):
    """
    Test successful login with valid credentials"""
    with allure.step("Navigate to login page and verify form is visible"):
        login_page.navigate(config.base_url).verify_login_form_visible()

    with allure.step("Login with valid credentials"):
        accounts_page = login_page.login(config.username, config.password)

    with allure.step("Check for any errors"):
        if login_page.is_error_visible():
            print(f"Login Error: {login_page.get_error_text()}")

    with allure.step("Verify successful login and accounts page"):
        accounts_page.verify_url(config.overview_url)
        accounts_page.verify_welcome_message(config.first_name)
        accounts_page.verify_accounts_table_visible()
        accounts_page.verify_accounts_exist()


# TC_UI_02 - Failed Login with Invalid Password
@allure.feature("Login")
@allure.story("TC_UI_02")
@allure.title("Failed login with invalid password")
@allure.severity(allure.severity_level.CRITICAL)
def test_failed_login(login_page: LoginPage, config):
    """
    Test un-successful login with invalid credentials"""
    with allure.step("Navigate to login page and verify form is visible"):
        login_page.navigate(config.base_url).verify_login_form_visible()

    with allure.step("Attempt login with invalid credentials"):
        login_page.login_with_invalid_credentials(
            config.username, config.invalid_password)

    with allure.step("Verify error message is displayed"):
        login_page.verify_error_message(
            "The username and password could not be verified.")

    with allure.step("Verify accounts overview is not visible"):
        accounts_page = AccountsOverviewPage(login_page.page)
        accounts_page.verify_accounts_overview_not_visible()
