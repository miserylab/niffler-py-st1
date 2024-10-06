from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.component.base_component import BaseComponent
from niffler_tests.utils.testing_steps import Step


class FriendsTable(BaseComponent):
    """Page component for friends table."""

    def __init__(self, page: Page):
        _locator = page.locator("//section[contains(@class,'main-content__section')]")
        super().__init__(_locator)
        self.page = page

    @Step("Get index of {username} in Username column")
    def get_username_index(self, username: str):
        usernames = self.get_element().locator("//tbody/tr/td[2]").all_text_contents()
        index = usernames.index(f"{username}") + 1
        return index

    @Step("Submit and decline buttons should be visible in Actions after invite")
    def submit_and_decline_buttons_should_be_visible_after_invite(self, username: str):
        index = self.get_username_index(username)
        action = self.get_element().locator(f"//tbody/tr[{index}]/td[4]")
        submit_button = action.locator("//div[@data-tooltip-id='submit-invitation']")
        decline_button = action.locator("//div[@data-tooltip-id='decline-invitation']")
        expect(submit_button).to_be_visible()
        expect(decline_button).to_be_visible()
        return self

    @Step("Submit invite of {username} in friend table")
    def submit_invite(self, username: str):
        index = self.get_username_index(username)
        submit_button = (
            self.get_element()
            .locator(f"//tbody/tr[{index}]/td[4]")
            .locator("//div[@data-tooltip-id='submit-invitation']")
        )
        submit_button.click()
        return self

    @Step("Decline invite of {username} in friend table")
    def decline_invite(self, username: str):
        index = self.get_username_index(username)
        decline_button = (
            self.get_element()
            .locator(f"//tbody/tr[{index}]/td[4]")
            .locator("//div[@data-tooltip-id='decline-invitation']")
        )
        decline_button.click()
        return self

    @Step("Remove friend with username={username} in friend table")
    def remove_friend(self, username: str):
        index = self.get_username_index(username)
        decline_button = (
            self.get_element().locator(f"//tbody/tr[{index}]/td[4]").locator("//div[@data-tooltip-id='remove-friend']")
        )
        decline_button.click()
        return self

    @Step("Check actions after friend submitted in friend table")
    def check_actions_after_friend_submitted(self, username: str, text: str):
        index = self.get_username_index(username)
        action = self.get_element().locator(f"//tbody/tr[{index}]/td[4]")
        remove_button = action.locator("//div[@data-tooltip-id='remove-friend']")
        expect(action).to_have_text(text)
        expect(remove_button).to_be_visible()
        return self

    @Step("Username {username} should not be present in friend table")
    def username_should_not_be_present(self, username: str):
        username_cell = self.get_element().locator(f"//tbody/tr/td[2][normalize-space()='{username}']")
        expect(username_cell).not_to_be_visible()
        return self
