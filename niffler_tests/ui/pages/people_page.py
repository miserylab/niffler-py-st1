from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.ui.pages.component.people_table import PeopleTable
from niffler_tests.utils.testing_steps import Step


class PeoplePage(BasePage):
    """Page object for people page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.table = PeopleTable(page)

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self.table.get_element().locator("//table//tbody//tr[1]/td[1]")).to_be_visible()
        return self
