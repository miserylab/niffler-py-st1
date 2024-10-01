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
        self._PROCEED_LOGIN_LINK = page.locator("//a[contains(@href, 'redirect')]")
        self._ERROR_MESSAGE = page.locator("//span[@class='form__error']")

    @Step("Get header on registration page")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER

    @Step("Fill Username and Password")
    def fill_registration_data(self, username: str, password: str, password_submit: str):
        self._USERNAME.fill(username)
        self._PASSWORD.fill(str(password))
        self._PASSWORD_SUBMIT.fill(str(password_submit))
        return self

    @Step("Submit register")
    def success_submit(self):
        self._SUBMIT_BUTTON.click()
        self._PROCEED_LOGIN_LINK.click()
        return self

    @Step("Submit register")
    def fail_submit(self):
        self._SUBMIT_BUTTON.click()
        return self

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self._USERNAME).to_be_visible()
        expect(self._PASSWORD).to_be_visible()
        expect(self._PASSWORD_SUBMIT).to_be_visible()
        expect(self._SUBMIT_BUTTON).to_be_visible()
        expect(self.get_header()).to_have_text("Welcome to Niffler. The coin keeper")
        return self

    @Step("Check error message")
    def check_error_message(self, error_message: str):
        expect(self._ERROR_MESSAGE).to_have_text(error_message)
