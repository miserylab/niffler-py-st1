import allure

from marks import User


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Регистрация")
@allure.tag("UI")
class TestRegistrationPage:
    @User.logout
    @allure.title("WEB: Пользователь может успешно зарегистрироваться в системе")
    def test_registration_success(self, envs, app, test_data, user_db):
        data = test_data["valid_user_data"]
        app.welcome_page.open(envs.app_url).wait_for_page_loaded()
        app.welcome_page.click_register()
        app.registration_page.wait_for_page_loaded()
        (
            app.registration_page.fill_registration_data(
                data["user_name"], data["password"], data["password"]
            ).success_submit()
        )
        app.login_page.fill_auth(data["user_name"], data["password"]).click_login()
        app.main_page.wait_for_page_loaded()

        user_entry = user_db.get_user_by_username(data["user_name"])
        assert user_entry
        assert user_entry.username == data["user_name"]
        assert user_entry.currency == "RUB"
        assert user_entry.firstname is None
        assert user_entry.surname is None
        assert user_entry.photo is None
        assert user_entry.photo_small is None

    @allure.title("WEB: При регистрации возникает ошибка, если пользователь с таким юзернеймом уже существует")
    def test_registration_user_registered(self, envs, app):
        app.welcome_page.open(envs.app_url).wait_for_page_loaded()
        app.welcome_page.click_register()
        app.registration_page.wait_for_page_loaded()
        app.registration_page.fill_registration_data(envs.username, envs.password, envs.password).fail_submit()
        app.registration_page.check_error_message(f"Username `{envs.username}` already exists")

    @allure.title("WEB: При регистрации возникает ошибка, если введены разные пароль и подтверждение пароля")
    def test_registration_passwords_not_equal(self, envs, app, test_data):
        data = test_data["valid_user_data"]
        app.welcome_page.open(envs.app_url).wait_for_page_loaded()
        app.welcome_page.click_register()
        app.registration_page.wait_for_page_loaded()
        (
            app.registration_page.fill_registration_data(
                data["user_name"], data["password"], data["password"] + "1"
            ).fail_submit()
        )
        app.registration_page.check_error_message("Passwords should be equal")
