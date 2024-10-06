import allure

from marks import User


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Аутентификация")
@allure.tag("UI")
class TestLoginPage:
    @User.logout
    @allure.title("WEB: Главная страница должна отображаться после логина новым юзером")
    def test_login_success(self, envs, app):
        app.welcome_page.open(envs.app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(envs.username, envs.password).click_login()

        app.main_page.wait_for_page_loaded()

    @allure.title("WEB: При неверно введенных логине/пароле пользователь остается неавторизованным")
    def test_invalid_login(self, envs, app):
        app.welcome_page.open(envs.app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(envs.username, envs.password + "BAD").click_login()

        app.login_page.check_alert("Bad credentials")
