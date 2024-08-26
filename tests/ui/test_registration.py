import allure
from faker import Faker
from playwright.sync_api import expect


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Регистрация")
@allure.tag("UI")
class TestRegistrationPage:

    def test_registration_success(self, app, user_test_data):
        data = user_test_data["valid_user_data"]

        app.welcome_page.open(app.URL)

        app.welcome_page.click_register()

        expect(app.registration_page.get_header()).to_have_text("Welcome to Niffler. The coin keeper")

        app.registration_page.fill_registration_data(data["user_name"], data["password"])

        app.registration_page.click_register()

