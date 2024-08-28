import allure
import pytest


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Регистрация")
@allure.tag("UI")
class TestRegistrationPage:
    @pytest.mark.usefixtures("logout")
    @allure.title("WEB: Пользователь может успешно зарегистрироваться в системе")
    def test_registration_success(self, app_url, app, test_data):
        data = test_data["valid_user_data"]
        app.welcome_page.open(app_url).wait_for_page_loaded()
        app.welcome_page.click_register()
        app.registration_page.wait_for_page_loaded()
        (
            app.registration_page.fill_registration_data(
                data["user_name"], data["password"], data["password"]
            ).success_submit()
        )
        app.login_page.fill_auth(data["user_name"], data["password"]).click_login()
        app.main_page.wait_for_page_loaded()

    @allure.title("WEB: При регистрации возникает ошибка, если пользователь с таким юзернеймом уже существует")
    def test_registration_user_registered(self, app_url, app, app_user):
        username, password = app_user
        app.welcome_page.open(app_url).wait_for_page_loaded()
        app.welcome_page.click_register()
        app.registration_page.wait_for_page_loaded()
        app.registration_page.fill_registration_data(username, password, password).fail_submit()
        app.registration_page.check_error_message(f"Username `{username}` already exists")

    @allure.title("WEB: При регистрации возникает ошибка, если введены разные пароль и подтверждение пароля")
    def test_registration_passwords_not_equal(self, app_url, app, test_data):
        data = test_data["valid_user_data"]
        app.welcome_page.open(app_url).wait_for_page_loaded()
        app.welcome_page.click_register()
        app.registration_page.wait_for_page_loaded()
        (
            app.registration_page.fill_registration_data(
                data["user_name"], data["password"], data["password"] + "1"
            ).fail_submit()
        )
        app.registration_page.check_error_message("Passwords should be equal")
