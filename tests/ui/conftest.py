import os

import dotenv
from faker import Faker

from niffler_tests.ui.core import App
from niffler_tests.utils.config import Config
import pytest

from niffler_tests.utils.utils import Utils


@pytest.fixture(autouse=True, scope="session")
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture
def user_test_data():
    faker = Faker("pt_BR")
    return {
        "valid_user_data": {
            "user_name": faker.user_name(),
            "password": Utils.get_timestamp(),
        }
    }


@pytest.fixture(scope="session")
def create_user(app, user_test_data):
    data = user_test_data["valid_user_data"]
    app.welcome_page.click_register()
    app.registration_page.fill_registration_data(data["user_name"], data["password"])
    app.registration_page.click_register()
    return data["user_name"], data["password"]


@pytest.fixture(scope="session")
def user():
    user = {"name": Config.username, "password": Config.password}
    return user


@pytest.fixture
def app(page, user):
    """Инициализация приложения и возврат экземпляра приложения."""
    return App(page, user)


@pytest.fixture
def login(app):
    app.login()
