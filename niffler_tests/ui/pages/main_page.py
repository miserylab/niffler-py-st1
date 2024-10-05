from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.ui.pages.component.add_spending import AddSpending
from niffler_tests.ui.pages.component.header import Header
from niffler_tests.ui.pages.component.spending_table import SpendingTable
from niffler_tests.utils.testing_steps import Step


class MainPage(BasePage):
    """Page object for login page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.spending_table = SpendingTable(page)
        self.spending = AddSpending(page)
        self.header = Header(page)
        self._HEADER = page.locator("//h1")
        self._FOOTER = page.locator("//footer[@class='footer']")

    @Step("Get header on main page")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER

    @Step("Get footer on main page")
    def get_footer(self):
        expect(self._FOOTER).to_be_visible()
        return self._FOOTER

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self.get_header()).to_have_text("Niffler. The coin keeper.")
        expect(self.get_footer()).to_have_text("Study project for QA Automation Advanced. 2023")

        expect(self.spending_table.get_element()).to_be_visible()
        expect(self.spending_table.get_header()).to_have_text("History of spendings")
        return self
