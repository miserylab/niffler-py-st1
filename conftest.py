import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright

from niffler_tests.clients.category_client import CategoryHttpClient


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def app_url(envs):
    return os.getenv("APP_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("AUTH_USERNAME"), os.getenv("AUTH_PASSWORD")


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def browser_context(browser_instance):
    context = browser_instance.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def auth(app_url, app_user, page):
    username, password = app_user
    print("Starting auth")
    page.goto(app_url)
    page.click("a[href*=redirect]")
    page.fill("input[name=username]", username)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")

    id_token = page.evaluate('window.sessionStorage.getItem("id_token")')
    print("Finished auth")
    return id_token


@pytest.fixture(scope="session")
def spends_client(gateway_url, auth) -> CategoryHttpClient:
    return CategoryHttpClient(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client) -> str:
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["category"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture
def logout(page):
    yield
    page.click("//button[@class='button-icon button-icon_type_logout']")
    expect(page.locator("//a[contains(@href, 'redirect')]")).to_be_visible()
