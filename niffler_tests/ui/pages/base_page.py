from playwright.sync_api import Page


class BasePage:
    """Page object для базовой страницы."""

    def __init__(self, page: Page) -> None:
        self.page = page
