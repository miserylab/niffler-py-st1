from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.base_page import BasePage
from niffler_tests.utils.testing_steps import Step


class ProfilePage(BasePage):
    """Page object for profile page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._USERNAME_LABEL = page.locator("//figcaption")
        self._NAME_INPUT = page.locator("//input[@name='firstname']")
        self._SURNAME_INPUT = page.locator("//input[@name='surname']")
        self._CATEGORY_INPUT = page.locator("//input[@name='category']")
        self._CURRENCY_SELECT = page.locator("//div[@class='select-wrapper'] ")
        self._SUBMIT_BUTTON = page.locator("//button[@type='submit']")
        self._CREATE_CATEGORY_BUTTON = page.locator("//button[contains(text(), 'Create')]")
        self._EXISTING_CATEGORIES_LIST = page.locator("//ul[@class='categories__list']//li")

    @Step("Check that page is loaded")
    def wait_for_page_loaded(self):
        expect(self._USERNAME_LABEL).to_be_visible()
        return self

    @Step("Set name: {name}")
    def set_name(self, name: str):
        self._NAME_INPUT.click()
        self._NAME_INPUT.fill(name)
        return self

    @Step("Set surname: {surname}")
    def set_surname(self, surname: str):
        self._SURNAME_INPUT.click()
        self._SURNAME_INPUT.fill(surname)
        return self

    @Step("Set currency: {currency}")
    def set_currency(self, currency: str):
        self._CURRENCY_SELECT.click()
        self.page.locator(f"//div[contains(@id,'react-select') and text()='{currency}']").click()
        return self

    @Step("Set category: {category}")
    def add_category(self, category: str):
        self._CATEGORY_INPUT.fill(category)
        self._CREATE_CATEGORY_BUTTON.click()
        return self

    @Step("Check category exists")
    def check_category_exists(self, category: str):
        expect(self._EXISTING_CATEGORIES_LIST.filter(has_text=category)).to_be_visible()
        return self

    @Step("Check username: {username}")
    def check_username(self, username: str):
        expect(self._USERNAME_LABEL).to_have_text(username)
        return self

    @Step("Check surname: {name}")
    def check_name(self, name: str):
        expect(self._NAME_INPUT).to_have_value(name)
        return self

    @Step("Check surname: {surname}")
    def check_surname(self, surname: str):
        expect(self._SURNAME_INPUT).to_have_value(surname)
        self.page.wait_for_timeout(5000)
        return self

    @Step("Check currency: {currency}")
    def check_currency(self, currency: str):
        expect(self._CURRENCY_SELECT).to_have_text(currency)
        return self

    @Step("Save profile")
    def submit_profile(self):
        self._SUBMIT_BUTTON.click()
        return self
