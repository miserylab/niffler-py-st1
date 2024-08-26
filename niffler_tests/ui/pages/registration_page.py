from allure_commons._allure import step
from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.utils.testing_steps import Step


class RegistrationPage(BasePage):
    """Page object for registration page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._HEADER = page.locator("//h1")
        self._USERNAME = page.locator("//input[@name='username']")
        self._PASSWORD = page.locator("//input[@name='password']")
        self._PASSWORD_SUBMIT = page.locator("//input[@name='passwordSubmit']")
        self._SUBMIT_BUTTON = page.locator("//button[@type='submit']")

    @Step("Get header on registration page")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER

    @Step("Fill Username and Password")
    def fill_registration_data(self, username: str, password: str):
        self._USERNAME.fill(username)
        self._PASSWORD.fill(str(password))
        self._PASSWORD_SUBMIT.fill(str(password))
        return self

    @Step("Click 'Sign Up'")
    def click_register(self):
        expect(self._SUBMIT_BUTTON).to_be_visible()
        self._SUBMIT_BUTTON.click()
