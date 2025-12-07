from playwright.sync_api import Page, expect


class AccountDetailsPage:

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.account_id_element = page.locator("#accountId")
        self.balance_element = page.locator("#balance")
        self.account_type_element = page.locator("#accountType")
        self.transactions_table = page.locator("#transactionTable")

    def verify_account_number(self, expected_account_number: str):
        """Verify account number matches expected value"""
        expect(self.account_id_element).to_have_text(expected_account_number)
        return self

    def verify_balance_visible(self):
        """Verify balance is displayed"""
        expect(self.balance_element).to_be_visible()
        return self

    def verify_balance_format(self):
        """Verify balance starts with $ symbol"""
        balance_text = self.balance_element.inner_text()
        assert balance_text.startswith("$"), "Balance should start with $"
        return self

    def get_balance(self) -> str:
        """Get the account balance text"""
        return self.balance_element.inner_text()

    def verify_account_type_visible(self):
        """Verify account type is displayed"""
        expect(self.account_type_element).to_be_visible()
        return self

    def get_account_type(self) -> str:
        """Get the account type"""
        return self.account_type_element.inner_text()

    def verify_transactions_table_visible(self):
        """Verify transactions table is displayed"""
        expect(self.transactions_table).to_be_visible()
        return self
