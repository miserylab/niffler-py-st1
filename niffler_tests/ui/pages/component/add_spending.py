from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.component.base_component import BaseComponent
from niffler_tests.utils.testing_steps import Step


class AddSpending(BaseComponent):
    """Page component for add spending section."""

    def __init__(self, page: Page):
        _locator = page.locator("//section[@class='main-content__section main-content__section-add-spending']")
        super().__init__(_locator)
        self.page = page
        self._HEADER = self.get_element().locator("//h2")
        self._CATEGORY_SELECT = self.get_element().locator("//input[contains(@id, 'react-select')]")
        self._AMOUNT_INPUT = self.get_element().locator("//input[@name='amount']")
        self._SPEND_DATE_SELECT = self.get_element().locator("//div[@class='react-datepicker__input-container']//input")
        self._DESCRIPTION_INPUT = self.get_element().locator("//input[@name='description']")
        self._ADD_SPENDING_BUTTON = self.get_element().locator("//button[@type='submit']")
        self._ERROR_TEXT = self.get_element().locator("//span[@class='form__error']")

    @Step("Set category {category}")
    def set_category(self, category: str):
        expect(self.get_element()).to_be_visible()
        self._CATEGORY_SELECT.click()
        self.get_element().locator(f"//div[@role='option'][text() = '{category}']").click()
        return self

    @Step("Set amount {amount}")
    def set_amount(self, amount: str):
        expect(self.get_element()).to_be_visible()
        self._AMOUNT_INPUT.fill(amount)
        return self

    @Step("Set date {date}")
    def set_date(self, date: str):
        expect(self.get_element()).to_be_visible()
        self._SPEND_DATE_SELECT.fill(date)
        self.page.keyboard.press("Enter")
        return self

    @Step("Set description {description}")
    def set_description(self, description: str):
        expect(self.get_element()).to_be_visible()
        self._DESCRIPTION_INPUT.fill(description)
        return self

    @Step("Add spending")
    def add_spending(self):
        self._ADD_SPENDING_BUTTON.click()
        return self

    @Step("Check error")
    def check_error(self, text: str):
        expect(self._ERROR_TEXT).to_have_text(text)
        return self
