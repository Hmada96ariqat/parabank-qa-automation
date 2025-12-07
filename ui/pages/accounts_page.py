from playwright.sync_api import Page, expect


class AccountsOverviewPage:

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.welcome_message = page.locator(".smallText")
        self.accounts_table = page.locator("#accountTable")
        self.account_rows = page.locator("#accountTable tbody tr")
        self.accounts_overview_heading = page.locator(
            'h1:has-text("Accounts Overview")')
        self.transfer_funds_link = page.locator("a[href='transfer.htm']")

    def verify_url(self, expected_url: str):
        """Verify current page URL"""
        expect(self.page).to_have_url(expected_url)
        return self

    def verify_welcome_message(self, first_name: str):
        """Verify welcome message contains customer name"""
        expect(self.welcome_message).to_be_visible()
        expect(
            self.welcome_message).to_contain_text(
            first_name,
            ignore_case=True)
        return self

    def verify_accounts_table_visible(self):
        """Verify accounts table is displayed"""
        expect(self.accounts_table).to_be_visible()
        return self

    def verify_accounts_exist(self):
        """Verify at least one account exists in the list"""
        expect(self.account_rows).not_to_have_count(0)
        return self

    def verify_accounts_overview_not_visible(self):
        """Verify accounts overview is not visible (used for failed login)"""
        expect(self.accounts_overview_heading).not_to_be_visible()
        return self

    def get_first_account_number(self) -> str:
        """Get the account number of the first account"""
        first_account_link = self.page.locator(
            "#accountTable tbody tr:first-child td:first-child a")
        expect(first_account_link).to_be_visible()
        return first_account_link.inner_text()

    def get_first_account_balance(self) -> str:
        """Get the balance of the first account"""
        balance = self.page.locator(
            "#accountTable tbody tr:first-child td:nth-child(2)")
        return balance.inner_text()

    def get_second_account_number(self) -> str:
        """Get the account number of the second account"""
        second_account_link = self.page.locator(
            "#accountTable tbody tr:nth-child(2) td:first-child a")
        expect(second_account_link).to_be_visible()
        return second_account_link.inner_text()

    def get_second_account_balance(self) -> str:
        """Get the balance of the second account"""
        balance = self.page.locator(
            "#accountTable tbody tr:nth-child(2) td:nth-child(2)")
        return balance.inner_text()

    def open_first_account(self):
        """Click the first account link to open account details"""
        first_account_link = self.page.locator(
            "#accountTable tbody tr:first-child td:first-child a")
        first_account_link.click()
        from .account_details_page import AccountDetailsPage
        return AccountDetailsPage(self.page)

    def navigate_to_transfer_funds(self):
        """Navigate to Transfer Funds page"""
        self.transfer_funds_link.click()
        from .transfer_page import TransferFundsPage
        return TransferFundsPage(self.page)

    def navigate(self, overview_url: str):
        """Navigate directly to accounts overview page"""
        self.page.goto(overview_url)
        return self
