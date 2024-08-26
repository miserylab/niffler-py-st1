from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.ui.pages.component.spending_table import SpendingTable
from niffler_tests.utils.testing_steps import Step


class MainPage(BasePage):
    """Page object for login page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.spending_table = SpendingTable(page)
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