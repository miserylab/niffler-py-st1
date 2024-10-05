import allure

from marks import User


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Аутентификация")
@allure.tag("UI")
class TestLoginPage:
    @User.logout
    @allure.title("WEB: Главная страница должна отображаться после логина новым юзером")
    def test_login_success(self, app_url, app):
        app.welcome_page.open(app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(app.username, app.password).click_login()

        app.main_page.wait_for_page_loaded()

    @allure.title("WEB: При неверно введенных логине/пароле пользователь остается неавторизованным")
    def test_invalid_login(self, app_url, app):
        app.welcome_page.open(app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(app.username, app.password + "BAD").click_login()

        app.login_page.check_alert("Bad credentials")
