import pytest
import yaml
from playwright.sync_api import Page, expect

# Load config from settings.yaml
def load_config():
    with open('config/settings.yaml', 'r') as file:
        return yaml.safe_load(file)

# TC_UI_01 - Successful Login with Valid Credentials
def test_successful_login(page: Page):
    
    # Load config
    config = load_config()
    base_url = config['ui_base_url']
    username = config['username']
    password = config['password']
    first_name = config['first_name'] # To verify welcome message
    # expected_welcome_name = config.get('expected_welcome_name', username)
    
    page.goto(base_url)
    
    # Verify login form is displayed
    username_field = page.locator("input[name='username']")
    password_field = page.locator("input[name='password']")
    login_button = page.locator("input[type='submit'][value='Log In']")
    expect(username_field).to_be_visible()
    expect(password_field).to_be_visible()


    username_field.fill(username)
    password_field.fill(password)

    login_button.click()


    # Check if login was successful or if there's an error
    error_message = page.locator(".error")
    if error_message.is_visible():
        print(f"Login Error: {error_message.inner_text()}")
    
    # Wait for overview page
    page.wait_for_url("**/overview.htm", timeout=10000)

    # Expected Result 1: User is redirected to Accounts Overview
    expect(page).to_have_url("https://parabank.parasoft.com/parabank/overview.htm")

    # Expected Result 2: Welcome message is displayed with customer name
    welcome_message = page.locator(".smallText")
    expect(welcome_message).to_be_visible() 
    expect(welcome_message).to_contain_text(["Welcome" + ' '+ first_name], ignore_case=True)
    # expect(welcome_message).to_contain_text(first_name, ignore_case=True)


    # Expected Result 3: Account list is visible
    accounts_table = page.locator("#accountTable")
    expect(accounts_table).to_be_visible()
    
    # Verify there are accounts in the list
    account_rows = page.locator("#accountTable tbody tr")
    expect(account_rows).not_to_have_count(0)
