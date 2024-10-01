from playwright.sync_api import Page, expect

from niffler_tests.utils.testing_steps import Step


class BasePage:
    """Page object для базовой страницы."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self._BASE_ALERT = page.locator("div .Toastify__toast-body")

    @Step("Check that success message appears: {expected_text}")
    def check_base_alert(self, expected_text: str):
        expect(self._BASE_ALERT).to_be_visible()
        expect(self._BASE_ALERT).to_have_text(expected_text)
        expect(self._BASE_ALERT).not_to_be_visible()
        return self
