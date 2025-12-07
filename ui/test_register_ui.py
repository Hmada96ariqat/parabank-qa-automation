'''ui/test_register_ui.py is for user registration tests in ParaBank application'''

import pytest
import yaml
from playwright.sync_api import Page, expect

# Load config from settings.yaml
def load_config():
    with open('config/settings.yaml', 'r') as file:
        return yaml.safe_load(file)

# Helper test - Register new user
def test_register_new_user(page: Page):
    """
    Register a new user in ParaBank
    This should be run first before login tests and if the user already exists, it's OK.
    user can still be used for login tests.
    """
    
    # Loading the confg file
    config = load_config()
    base_url = config['ui_base_url']
    username = config['username']
    password = config['password']
    first_name = config['first_name']
    last_name = config['last_name']
    street = config['street']
    city = config['city']
    state = config['state']
    zip_code = config['zip_code']
    phone = config['phone']
    ssn = config['ssn']


    page.goto(f"{base_url}/register.htm")
    # Assert that the ppage is loaded
    expect(page.locator("form#customerForm")).to_be_visible()
    expect(page.locator("input[name='customer.firstName']")).to_be_visible()


    # Fill in registration form with <input> CSS elements
    page.locator("input[name='customer.firstName']").fill(first_name)
    page.locator("input[name='customer.lastName']").fill(last_name)
    page.locator("input[name='customer.address.street']").fill(street)
    page.locator("input[name='customer.address.city']").fill(city)
    page.locator("input[name='customer.address.state']").fill(state)
    page.locator("input[name='customer.address.zipCode']").fill(zip_code)
    page.locator("input[name='customer.phoneNumber']").fill(phone)
    page.locator("input[name='customer.ssn']").fill(ssn)
        
    # Username and password
    page.locator("input[name='customer.username']").fill(username)
    page.locator("input[name='customer.password']").fill(password)
    page.locator("input[name='repeatedPassword']").fill(password)
    page.locator("input[value='Register']").click()


    # Check if registration was successful
    success_message = page.locator("#rightPanel h1")
    if success_message.is_visible():
        print(f"Registration result: {success_message.inner_text()}")

    # Check for error - user might already exist
    error = page.locator(".error")
    if error.is_visible():
        error_text = error.inner_text()
        print(f"Registration notice: {error_text}")
        # If This username already exists, that's OK - we can still use them
        if "This username already exists" in error_text.lower():
            print("User already registered - this is OK, we can proceed with login tests")
