from playwright.sync_api import Page, expect


class RegisterPage:
    """Page Object Model for ParaBank Registration Page"""

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.registration_form = page.locator("form#customerForm")
        self.first_name_field = page.locator(
            "input[name='customer.firstName']")
        self.last_name_field = page.locator("input[name='customer.lastName']")
        self.street_field = page.locator(
            "input[name='customer.address.street']")
        self.city_field = page.locator("input[name='customer.address.city']")
        self.state_field = page.locator("input[name='customer.address.state']")
        self.zip_code_field = page.locator(
            "input[name='customer.address.zipCode']")
        self.phone_field = page.locator("input[name='customer.phoneNumber']")
        self.ssn_field = page.locator("input[name='customer.ssn']")
        self.username_field = page.locator("input[name='customer.username']")
        self.password_field = page.locator("input[name='customer.password']")
        self.confirm_password_field = page.locator(
            "input[name='repeatedPassword']")
        self.register_button = page.locator("input[value='Register']")
        self.success_message = page.get_by_text(
            'Your account was created successfully. You are now logged in.')
        self.error_message = page.locator(".error")

    def navigate(self, base_url: str):
        """Navigate to the registration page"""
        self.page.goto(f"{base_url}/register.htm")
        return self

    def verify_registration_form_visible(self):
        """Verify that registration form is visible"""
        expect(self.registration_form).to_be_visible()
        expect(self.first_name_field).to_be_visible()
        return self

    def fill_registration_form(
            self,
            first_name: str,
            last_name: str,
            street: str,
            city: str,
            state: str,
            zip_code: str,
            phone: str,
            ssn: str,
            username: str,
            password: str):
        """Fill out the complete registration form"""
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.street_field.fill(street)
        self.city_field.fill(city)
        self.state_field.fill(state)
        self.zip_code_field.fill(zip_code)
        self.phone_field.fill(phone)
        self.ssn_field.fill(ssn)
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.confirm_password_field.fill(password)
        return self

    def click_register(self):
        """Click the register button"""
        self.register_button.click()
        return self

    def register(self, first_name: str, last_name: str, street: str,
                 city: str, state: str, zip_code: str, phone: str,
                 ssn: str, username: str, password: str):
        """Complete registration flow"""
        self.fill_registration_form(
            first_name,
            last_name,
            street,
            city,
            state,
            zip_code,
            phone,
            ssn,
            username,
            password)
        self.click_register()
        return self

    def is_success_message_visible(self) -> bool:
        """Check if success message is visible"""
        return self.success_message.is_visible()

    def is_error_visible(self) -> bool:
        """Check if error message is visible"""
        return self.error_message.is_visible()

    def get_error_text(self) -> str:
        """Get error message text"""
        if self.is_error_visible():
            return self.error_message.inner_text()
        return ""
