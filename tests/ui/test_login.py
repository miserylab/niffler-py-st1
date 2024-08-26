import pytest
import allure
from playwright.sync_api import expect

@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Аутентификация")
@allure.tag("UI")
class TestLoginPage:

    @allure.title("WEB: Главная страница должна отображаться после логина новым юзером")
    def test_login_success(self, app):
        app.welcome_page.open(app.URL)
        app.welcome_page.click_login()
        app.login_page.fill_auth(app.username, app.password).click_login()

        expect(app.main_page.get_header()).to_have_text("Niffler. The coin keeper.")
        expect(app.main_page.get_footer()).to_have_text("Study project for QA Automation Advanced. 2023")

        expect(app.main_page.spending_table.get_element()).to_be_visible()
        expect(app.main_page.spending_table.get_header()).to_have_text("History of spendings")

    @allure.title("WEB: При неверно введенных логине/пароле пользователь остается неавторизованным")
    def test_invalid_login(self, app):
        app.welcome_page.open(app.URL)
        app.welcome_page.click_login()
        app.login_page.fill_auth(app.username, app.password + "BAD").click_login()

        app.login_page.check_alert("Bad credentials")