from playwright.async_api import Page
from playwright.sync_api import expect

from niffler_tests.ui.pages.component.base_component import BaseComponent
from niffler_tests.utils.testing_steps import Step


class Header(BaseComponent):
    """Page component for header."""

    def __init__(self, page: Page):
        _locator = page.locator("//header")
        super().__init__(_locator)
        self.page = page
        self._MAIN_PAGE_BUTTON = self.get_element().locator("//li[@data-tooltip-id='main']//img")
        self._FRIENDS_PAGE_BUTTON = self.get_element().locator("//li[@data-tooltip-id='friends']//img")
        self._PEOPLE_PAGE_BUTTON = self.get_element().locator("//li[@data-tooltip-id='people']//img")
        self._LOGOUT_BUTTON = self.get_element().locator("//li//div[@data-tooltip-id='logout']//button")

    @Step("Go to main page from header")
    def to_main_page(self):
        self._MAIN_PAGE_BUTTON.click()
        return self

    @Step("Go to friends page from header")
    def to_friends_page(self):
        self._FRIENDS_PAGE_BUTTON.click()
        return self

    @Step("Go to people page from header")
    def to_people_page(self):
        self._PEOPLE_PAGE_BUTTON.click()
        return self

    @Step("Click Logout")
    def click_logout(self):
        self._LOGOUT_BUTTON.click()
        expect(self.page.locator("//a[contains(@href, 'redirect')]")).to_be_visible()
        return self
