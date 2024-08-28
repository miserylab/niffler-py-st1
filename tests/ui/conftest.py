import pytest
from faker import Faker

from niffler_tests.ui.core import App


@pytest.fixture
def test_data():
    faker = Faker("pt_BR")
    return {
        "valid_user_data": {
            "user_name": faker.user_name(),
            "password": faker.password(),
        },
        "profile_all_fields_data": {
            "name": faker.first_name(),
            "surname": faker.last_name(),
            "currency": "EUR",
        },
        "category_data": {
            "name": faker.last_name(),
        },
    }


@pytest.fixture
def app(page, app_user):
    """Инициализация приложения и возврат экземпляра приложения."""
    return App(page, app_user)


@pytest.fixture
def register_new_user_and_login(app_url, app, test_data):
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


@pytest.fixture
def register_new_user(app_url, app, test_data):
    data = test_data["valid_user_data"]
    print("Start registering new user")
    app.welcome_page.open(app_url).wait_for_page_loaded()
    app.welcome_page.click_register()
    app.registration_page.wait_for_page_loaded()
    (
        app.registration_page.fill_registration_data(
            data["user_name"], data["password"], data["password"]
        ).success_submit()
    )
    print("User registered successfully")
    return data["user_name"], data["password"], data["password"]
