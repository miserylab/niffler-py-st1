from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.component.base_component import BaseComponent
from niffler_tests.utils.testing_steps import Step


class SpendingTable(BaseComponent):
    """Page component for spending table."""

    def __init__(self, page: Page):
        _locator = page.locator("//section[contains(@class,'main-content__section-history')]")
        super().__init__(_locator)
        self._HEADER = self.get_element().locator("//h2")

    @Step("Get header in spending table")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER
