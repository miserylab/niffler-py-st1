from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.ui.pages.component.people_table import PeopleTable
from niffler_tests.utils.config import Config
from niffler_tests.utils.testing_steps import Step


class PeoplePage(BasePage):
    """Page object for people page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.people_table = PeopleTable(page)
        self.url = Config.app_url + "/people"

    @Step("Open people page")
    def open(self):
        self.page.goto(self.url)
        return self

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self.people_table.get_element()).to_be_visible()
        return self
