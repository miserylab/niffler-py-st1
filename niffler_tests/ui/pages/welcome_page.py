from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.utils.testing_steps import Step


class WelcomePage(BasePage):
    """Page object for welcome page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._HEADER = page.locator("//h1")
        self._LOGIN_BUTTON = page.locator("//a[contains(@href, 'redirect')]")
        self._REGISTER_BUTTON = page.locator("//a[contains(@href, 'register')]")

    @Step("Get header on welcome page")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER

    @Step("Open main page")
    def open(self, url: str):
        self.page.goto(url)
        return self

    @Step("Click 'Login'")
    def click_login(self):
        self._LOGIN_BUTTON.click()

    @Step("Click 'Register'")
    def click_register(self):
        self._REGISTER_BUTTON.click()

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self._LOGIN_BUTTON).to_be_visible()
        expect(self._REGISTER_BUTTON).to_be_visible()
        return self
