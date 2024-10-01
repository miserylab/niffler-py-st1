from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.utils.testing_steps import Step


class LoginPage(BasePage):
    """Page object for login page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._HEADER = page.locator("//h1")
        self._USERNAME_FIELD = page.locator("//input[@name='username']")
        self._PASSWORD_FIELD = page.locator("//input[@name='password']")
        self._SIGN_IN_BUTTON = page.locator("//button[@type='submit']")
        self._SIGN_UP_BUTTON = page.locator("//a[@href='/register']")
        self._ALERT = page.locator("//p[@class='form__error']")

    @Step("Click 'Sign In'")
    def click_login(self):
        expect(self._SIGN_IN_BUTTON).to_be_visible()
        self._SIGN_IN_BUTTON.click()

    @Step("Click 'Sign Up'")
    def click_register(self):
        expect(self._SIGN_UP_BUTTON).to_be_visible()
        self._SIGN_UP_BUTTON.click()

    @Step("Fill Username and Password")
    def fill_auth(self, username: str, password: str):
        self._USERNAME_FIELD.fill(username)
        self._PASSWORD_FIELD.fill(password)
        return self

    @Step("Check alert")
    def check_alert(self, error_name: str):
        expect(self._ALERT).to_have_text(error_name)

    @Step("Get header on login page")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER
