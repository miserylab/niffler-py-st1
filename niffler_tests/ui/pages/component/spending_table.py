from playwright.sync_api import Page, expect

from niffler_tests.ui.pages.component.base_component import BaseComponent
from niffler_tests.utils.testing_steps import Step


class SpendingTable(BaseComponent):
    """Page component for spending table."""

    def __init__(self, page: Page):
        _locator = page.locator("//section[contains(@class,'main-content__section-history')]")
        super().__init__(_locator)
        self._HEADER = self.get_element().locator("//h2")
        self._TABLE = self.get_element().locator("//table[@class='table spendings-table']")
        self._DELETE_SELECTED_BUTTON = self.get_element().locator("//section[@class='spendings__bulk-actions']/button")

    @Step("Get header in spending table")
    def get_header(self):
        expect(self._HEADER).to_be_visible()
        return self._HEADER

    @Step("Title should have text {expected_text}")
    def title_should_have_text(self, expected_text):
        expect(self._HEADER).to_be_visible()
        expect(self._HEADER).to_have_text(expected_text)

    @Step("Table should contain value {value}")
    def should_contain_value(self, value):
        expect(self._TABLE.locator("//tbody")).to_contain_text(value)

    @Step("Select entry checkbox by id={spend_id}")
    def select_entry_checkbox(self, spend_id):
        entry = self.get_element().locator(f"//tbody//input[@type='checkbox'][@value='{spend_id}']")
        entry.scroll_into_view_if_needed()
        expect(entry).to_be_visible()
        entry.click()

    @Step("Get table entries")
    def get_entries(self):
        return self._TABLE.locator("//tbody//tr").count()

    def get_column_index_by_name(self, column_name: str):
        #     //section[contains(@class,'main-content__section-history')]//thead/tr/th
        columns = (
            self.get_element()
            .locator("//section[contains(@class,'main-content__section-history')]//thead/tr/th[text()='Date']")
            .all_text_contents()
        )
        index = columns.index(f"{column_name}") + 1
        return index

    def get_entry_index_by_id(self, id: int):
        # get list of usernames from Username column
        ids = (
            self.get_element()
            .locator("//table[@class='spendings-table']//tbody//input[@type='checkbox']")
            .all_text_contents()
        )
        print(f"id: {ids}")
        index = ids.index(f"{id}") + 1
        #     //section[contains(@class,'main-content__section-history')]//tbody/tr/td[1]/
        # input[@value= "7104fce5-531a-462b-b19e-69f7805d830d"]
        return index

    @Step("Get value in {columnname}")
    def assert_value(self, entry_id: int, columnname, expected_value):
        tr = self.get_entry_index_by_id(entry_id)
        td = self.get_column_index_by_name(columnname)
        entry = self.get_element().locator(f"//tbody/tr[{tr}]/td[{td}]")
        expect(entry).to_have_value(expected_value)

    @Step("Click delete selected button")
    def delete_selected(self):
        self._DELETE_SELECTED_BUTTON.click()
        return self

    @Step("Spending table should be empty")
    def spending_table_is_empty(self):
        expect(self.get_element().locator(".spendings-table tbody tr")).to_have_count(0)
        expect(self.get_element().locator(".spendings__content")).to_contain_text("No spendings provided yet!")
