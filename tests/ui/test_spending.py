import allure

from marks import Actions, GenerateData, Pages, User
from niffler_tests.utils.utils import Utils


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Добавление расходов")
@allure.tag("UI")
class TestSpendingPage:
    @allure.title("WEB: Пользователь имеет возможность добавить трату")
    @GenerateData.category("Friends")
    @Actions.delete_all_spendings
    def test_add_spending(self, app, category):
        app.reload_page()

        app.main_page.spending.set_category(category)
        app.main_page.spending.set_amount("121.9")
        app.main_page.spending.set_date(Utils.get_date())
        description = f"test {Utils.get_timestamp()}"
        app.main_page.spending.set_description(description)
        app.main_page.spending.add_spending()

        app.main_page.check_base_alert("Spending successfully added")

        app.main_page.spending_table.should_contain_value(description)

    @allure.title("WEB: Нельзя добавить трату с будущей датой")
    @GenerateData.category("Friends")
    def test_add_spending_future_date(self, app, category):
        app.reload_page()

        app.main_page.spending.set_category(category)
        app.main_page.spending.set_amount("121.9")
        app.main_page.spending.set_date(Utils.get_date(5))
        description = f"test {Utils.get_timestamp()}"
        app.main_page.spending.set_description(description)
        app.main_page.spending.add_spending()

        app.main_page.spending.check_error("You can not pick future date")

    @allure.title("WEB: Нельзя добавить трату пустой категорией")
    @User.login
    def test_add_spending_empty_category(self, app):
        app.main_page.spending.set_amount("121.9")
        app.main_page.spending.set_date(Utils.get_date())
        description = f"test {Utils.get_timestamp()}"
        app.main_page.spending.set_description(description)
        app.main_page.spending.add_spending()

        app.main_page.spending.check_error("Category is required")

    @allure.title("WEB: Нельзя добавить трату с пустым значением суммы")
    @GenerateData.category("Friends")
    def test_add_spending_empty_amount(self, app, category):
        app.reload_page()

        app.main_page.spending.set_category(category)
        app.main_page.spending.set_date(Utils.get_date())
        description = f"test {Utils.get_timestamp()}"
        app.main_page.spending.set_description(description)
        app.main_page.spending.add_spending()

        app.main_page.spending.check_error("Amount is required")

    @User.logout
    @allure.title("WEB: Пользователь имеет возможность отредактировать трату")
    def test_edit_spending(self):
        pass

    @Pages.main_page
    def test_spending_title_exists(self, app):
        app.main_page.spending_table.title_should_have_text("History of spendings")

    TEST_CATEGORY = "school"

    @allure.title("WEB: Пользователь имеет возможность удалить трату")
    @GenerateData.category(TEST_CATEGORY)
    @GenerateData.spends(
        {
            "amount": "108.51",
            "description": "QA.GURU Python Advanced 1",
            "category": TEST_CATEGORY,
            "spendDate": f"{Utils.get_current_date()}",
            "currency": "RUB",
        }
    )
    def test_spending_should_be_deleted_after_table_action(self, category, spends, app):
        app.reload_page()

        app.main_page.spending_table.should_contain_value("QA.GURU Python Advanced 1")

        app.main_page.spending_table.select_entry_checkbox(spends["id"])

        app.main_page.spending_table.delete_selected()

        app.main_page.spending_table.spending_table_is_empty()
