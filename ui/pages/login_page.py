from .accounts_page import AccountsOverviewPage
from playwright.sync_api import Page, expect


class LoginPage:
    # POM file for Login Page
    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.username_field = page.locator("input[name='username']")
        self.password_field = page.locator("input[name='password']")
        self.login_button = page.locator(
            "input[type='submit'][value='Log In']")
        self.error_message = page.locator(".error")

    def navigate(self, base_url: str):
        # Navigate to the login page
        self.page.goto(base_url)
        return self

    def verify_login_form_visible(self):
        # Verify that login form elements are visible
        expect(self.username_field).to_be_visible()
        expect(self.password_field).to_be_visible()
        expect(self.login_button).to_be_visible()
        return self

    def enter_credentials(self, username: str, password: str):
        # Enter username and password
        self.username_field.fill(username)
        self.password_field.fill(password)
        return self

    def click_login(self):
        # Click the login button
        self.login_button.click()

        return AccountsOverviewPage(self.page)

    def login(self, username: str, password: str):
        # Complete login flow with valid credentials
        self.enter_credentials(username, password)

        return self.click_login()

    def login_with_invalid_credentials(self, username: str, password: str):
        # Attempt login with invalid credentials
        self.enter_credentials(username, password)
        self.login_button.click()

        return self

    def verify_error_message(self, expected_message: str):
        # Verify error message is displayed
        expect(self.error_message).to_be_visible()
        expect(
            self.error_message).to_contain_text(
            expected_message,
            ignore_case=True)
        return self

    def is_error_visible(self) -> bool:
        # Check if error message is visible
        return self.error_message.is_visible()

    def get_error_text(self) -> str:
        # Get error message text
        if self.is_error_visible():
            return (self.error_message.inner_text()
                    if self.is_error_visible() else "")
