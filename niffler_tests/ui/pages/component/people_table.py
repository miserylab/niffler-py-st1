from playwright.async_api import Page
from playwright.sync_api import expect

from niffler_tests.ui.pages.component.base_component import BaseComponent
from niffler_tests.utils.testing_steps import Step


class PeopleTable(BaseComponent):
    """Page component for people table."""

    def __init__(self, page: Page):
        _locator = page.locator("//section[contains(@class,'main-content__section')]")
        super().__init__(_locator)
        self.page = page
        self._ADD_FRIEND_BUTTON = self.get_element().locator("//div[@data-tooltip-id='add-friend']")

    @Step("Get index of {username} in Username column")
    def get_username_index(self, username: str):
        # get list of usernames from Username column
        usernames = self.get_element().locator("//tbody/tr/td[2]").all_text_contents()
        index = usernames.index(f"{username}") + 1
        return index

    @Step("Add friend {username} on people table")
    def add_friend(self, username: str):
        index = self.get_username_index(username)
        add_button = (
            self.get_element().locator(f"//tbody/tr[{index}]/td[4]").locator("//div[@data-tooltip-id='add-friend']")
        )
        add_button.click()
        return self

    @Step("Check add button state on people table")
    def check_add_button(self, username: str, text: str):
        index = self.get_username_index(username)
        action = self.get_element().locator(f"//tbody/tr[{index}]/td[4]")
        expect(action).to_have_text(text)
        return self
