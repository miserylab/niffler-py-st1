from playwright.sync_api import Locator


class BaseComponent:
    def __init__(self, element: Locator):
        self._element = element

    def get_element(self) -> Locator:
        return self._element
