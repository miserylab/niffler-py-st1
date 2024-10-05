from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.ui.pages.component.friends_table import FriendsTable
from niffler_tests.utils.testing_steps import Step


class FriendsPage(BasePage):
    """Page object for friends page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.table = FriendsTable(page)

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self.table.get_element()).to_be_visible()
        return self
