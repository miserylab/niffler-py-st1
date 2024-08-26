from allure_commons._allure import step
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
    def open(self, url: str) -> None:
        self.page.goto(url)
        expect(self.get_header()).to_have_text("Welcome to magic journey with Niffler. The coin keeper")


    @Step("Click 'Login'")
    def click_login(self):
        expect(self._LOGIN_BUTTON).to_be_visible()
        self._LOGIN_BUTTON.click()
        expect(self.get_header()).to_have_text("Welcome to Niffler. The coin keeper")

    @Step("Click 'Register'")
    def click_register(self):
        expect(self._REGISTER_BUTTON).to_be_visible()
        self._REGISTER_BUTTON.click()
