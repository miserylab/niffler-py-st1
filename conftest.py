import logging
import os

import allure
import pytest
from dotenv import load_dotenv
from faker import Faker
from playwright.sync_api import Browser, Page, Playwright, expect

from niffler_tests.clients.invitation_client import InvitationHttpClient
from niffler_tests.clients.registration_client import RegistrationHttpClient
from niffler_tests.clients.spends_client import SpendsHttpClient
from niffler_tests.databases.spend_db import SpendDb
from niffler_tests.databases.user_db import UserDb
from niffler_tests.models.config import Envs

faker = Faker("pt_BR")


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        app_url=os.getenv("APP_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        auth_url=os.getenv("AUTH_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        user_db_url=os.getenv("USER_DB_URL"),
        username=os.getenv("AUTH_USERNAME"),
        password=os.getenv("AUTH_PASSWORD"),
    )


@pytest.fixture
def browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    new_page = browser.new_page()
    yield new_page
    new_page.close()


@pytest.fixture
def auth(envs, page):
    logging.info(f"Starting auth with username = {envs.username}, password = {envs.password}")
    page.goto(envs.app_url)
    page.click("a[href*=redirect]")
    page.fill("input[name=username]", envs.username)
    page.fill("input[name=password]", envs.password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")

    id_token = page.evaluate('window.sessionStorage.getItem("id_token")')
    assert id_token
    logging.info("Finished auth")
    return id_token


@pytest.fixture(scope="function")
def registration_client(envs) -> RegistrationHttpClient:
    return RegistrationHttpClient(envs.auth_url)


@pytest.fixture(scope="function")
def user_db(envs) -> UserDb:
    return UserDb(envs.user_db_url)


@pytest.fixture
def get_token(registration_client, envs, page):
    username = faker.user_name()
    password = faker.password()
    registration_client.register(username=username, password=password)
    logging.info(f"Starting auth with username = {username}, password = {password}")
    page.goto(envs.app_url)
    page.click("a[href*=redirect]")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")
    id_token = page.evaluate('window.sessionStorage.getItem("id_token")')
    assert id_token
    logging.info("Finished auth")
    return id_token, username, password


@pytest.fixture
@allure.step("Delete user with accepted friendship from db")
def delete_user_with_friendship(get_token, user_db):
    yield
    _, username, _ = get_token
    user_entry = user_db.get_user_by_username(username)
    friendship_entry = user_db.get_friendship_by_addressee_id(user_entry.id)
    friendship_entry_1 = user_db.get_friendship_by_requester_id(user_entry.id)
    user_db.delete_friendship(friendship_entry.requester_id, friendship_entry.addressee_id)
    user_db.delete_friendship(friendship_entry_1.requester_id, friendship_entry_1.addressee_id)
    user_db.delete_user_by_id(user_entry.id)


@pytest.fixture
@allure.step("Delete user with declined or removed friendship from db")
def delete_user_wo_friendship(get_token, user_db):
    yield
    _, username, _ = get_token
    user_entry = user_db.get_user_by_username(username)
    friendship_entry = user_db.get_friendship_by_requester_id(user_entry.id)
    user_db.delete_friendship(friendship_entry.requester_id, friendship_entry.addressee_id)
    user_db.delete_user_by_id(user_entry.id)


@pytest.fixture(scope="function")
def invitation_client(envs, get_token) -> InvitationHttpClient:
    token = get_token[0]
    return InvitationHttpClient(envs.gateway_url, token)


@pytest.fixture(params=[])
def send_invitation(request, invitation_client):
    invitation_client.send_invitation(request.param)


@pytest.fixture(scope="function")
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope="function")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def category(request, spends_client, spend_db) -> str:
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture
def logout_user(get_token, page):
    _, username, _ = get_token
    logging.info(f"Logout user with {username}")
    page.click("//button[@class='button-icon button-icon_type_logout']")
    expect(page.locator("//a[contains(@href, 'redirect')]")).to_be_visible()


@pytest.fixture
def ui_logout(envs, page):
    yield
    logging.info(f"Logout with username={envs.username}")
    page.click("//button[@class='button-icon button-icon_type_logout']")
    expect(page.locator("//a[contains(@href, 'redirect')]")).to_be_visible()


@pytest.fixture()
def main_page_fixture(auth, envs, page):
    page.goto(envs.app_url)
    return page


@pytest.fixture()
def api_delete_all_spendings(auth, page, spends_client):
    yield
    current_spends = spends_client.get_spends()
    print(current_spends)
    spend_ids = [spend_entry.id for spend_entry in current_spends]
    for spend_id in spend_ids:
        spends_client.remove_spends([spend_id])
        logging.info("Delete spendings in fixture")
