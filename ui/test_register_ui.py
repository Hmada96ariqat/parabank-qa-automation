import pytest
import allure
from ui.pages import RegisterPage


# Register new user (runs first)
@pytest.mark.first
@allure.feature("Registration")
@allure.story("User Registration")
@allure.title("Register a new user in ParaBank")
@allure.severity(allure.severity_level.BLOCKER)
def test_register_new_user(register_page: RegisterPage, config):
    """
    Register a new user in ParaBank
    This should be run first before login tests
    """

    with allure.step("Navigate to register page and verify form"):
        register_page.navigate(config.base_url).verify_registration_form_visible()

    with allure.step("Complete registration form with user details"):
        register_page.register(
            first_name=config.first_name,
            last_name=config.last_name,
            street=config.street,
            city=config.city,
            state=config.state,
            zip_code=config.zip_code,
            phone=config.phone,
            ssn=config.ssn,
            username=config.username,
            password=config.password
        )

    with allure.step("Check registration result"):
        if register_page.is_success_message_visible():
            print("Registration successful")

        # Check for error - user might already exist
        if register_page.is_error_visible():
            error_text = register_page.get_error_text()
            print(f"Registration notice: {error_text}")
            # If user already exists, that's OK - we can still use them
            if "already exists" in error_text.lower():
                print("User already registered - this is OK, we can "
                      "proceed with login tests")
