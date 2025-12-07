from playwright.sync_api import Page, expect


class TransferFundsPage:
    """Page Object Model for ParaBank Transfer Funds Page"""

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.amount_field = page.locator("#amount")
        self.from_account_dropdown = page.locator("#fromAccountId")
        self.to_account_dropdown = page.locator("#toAccountId")
        self.transfer_button = page.locator("input[value='Transfer']")
        self.confirmation_message = page.locator("#showResult")

    def enter_amount(self, amount: float):
        """Enter transfer amount"""
        self.amount_field.fill(str(amount))
        return self

    def select_from_account(self, account_number: str):
        """Select source account from dropdown"""
        self.from_account_dropdown.select_option(account_number)
        return self

    def select_to_account(self, account_number: str):
        """Select destination account from dropdown"""
        self.to_account_dropdown.select_option(account_number)
        return self

    def click_transfer(self):
        """Click transfer button"""
        self.transfer_button.click()
        return self

    def transfer(self, amount: float, from_account: str, to_account: str):
        """Complete transfer flow"""
        self.enter_amount(amount)
        self.select_from_account(from_account)
        self.select_to_account(to_account)
        self.click_transfer()
        return self

    def verify_transfer_complete(self):
        """Verify transfer completion message is displayed"""
        expect(self.confirmation_message).to_be_visible()
        expect(
            self.confirmation_message).to_contain_text(
            "Transfer Complete",
            ignore_case=True)
        return self

    def get_confirmation_message(self) -> str:
        """Get confirmation message text"""
        return self.confirmation_message.inner_text()
