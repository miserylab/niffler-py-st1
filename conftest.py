import logging
import os

import pytest
from dotenv import load_dotenv
from faker import Faker
from playwright.sync_api import Browser, Page, Playwright, expect

from niffler_tests.clients.invitation_client import InvitationHttpClient
from niffler_tests.clients.registration_client import RegistrationHttpClient
from niffler_tests.clients.spends_client import SpendsHttpClient
from niffler_tests.utils.config import Config

faker = Faker("pt_BR")


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def app_url(envs):
    return os.getenv("APP_URL")


@pytest.fixture(scope="session")
def auth_url(envs):
    return os.getenv("AUTH_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("AUTH_USERNAME"), os.getenv("AUTH_PASSWORD")


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
def auth(app_url, app_user, page):
    username, password = app_user
    logging.info(f"Starting auth with username = {username}, password = {password}")
    page.goto(app_url)
    page.click("a[href*=redirect]")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")

    id_token = page.evaluate('window.sessionStorage.getItem("id_token")')
    assert id_token
    logging.info("Finished auth")
    return id_token


@pytest.fixture(scope="function")
def registration_client(auth_url) -> RegistrationHttpClient:
    return RegistrationHttpClient(auth_url)


@pytest.fixture
def get_token(registration_client, app_url, page):
    username = faker.user_name()
    password = faker.password()
    registration_client.register(username=username, password=password)
    logging.info(f"Starting auth with username = {username}, password = {password}")
    page.goto(app_url)
    page.click("a[href*=redirect]")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")
    id_token = page.evaluate('window.sessionStorage.getItem("id_token")')
    assert id_token
    logging.info("Finished auth")
    return id_token, username, password


@pytest.fixture(scope="function")
def invitation_client(gateway_url, get_token) -> InvitationHttpClient:
    token = get_token[0]
    return InvitationHttpClient(gateway_url, token)


@pytest.fixture(params=[])
def send_invitation(request, invitation_client):
    invitation_client.send_invitation(request.param)


@pytest.fixture(scope="function")
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client) -> str:
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["category"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    current_spends = spends_client.get_spends()
    print(current_spends)
    spend_ids = [spend["id"] for spend in current_spends]
    if spend["id"] in spend_ids:
        logging.info("Delete spends in fixture")
        spends_client.remove_spends([spend["id"]])


@pytest.fixture
def logout_user(get_token, page):
    _, username, _ = get_token
    logging.info(f"Logout user with {username}")
    page.click("//button[@class='button-icon button-icon_type_logout']")
    expect(page.locator("//a[contains(@href, 'redirect')]")).to_be_visible()


@pytest.fixture
def ui_logout(page):
    yield
    logging.info(f"Logout with username={Config.username}")
    page.click("//button[@class='button-icon button-icon_type_logout']")
    expect(page.locator("//a[contains(@href, 'redirect')]")).to_be_visible()


@pytest.fixture()
def main_page_fixture(auth, app_url, page):
    page.goto(app_url)
    return page


@pytest.fixture()
def api_delete_all_spendings(auth, page, spends_client):
    yield
    current_spends = spends_client.get_spends()
    print(current_spends)
    spend_ids = [spend_entry["id"] for spend_entry in current_spends]
    for spend_id in spend_ids:
        spends_client.remove_spends([spend_id])
        logging.info("Delete spendings in fixture")
