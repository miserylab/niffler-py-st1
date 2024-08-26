from niffler_tests.ui.pages.login_page import LoginPage
from niffler_tests.ui.pages.main_page import MainPage
from niffler_tests.ui.pages.registration_page import RegistrationPage
from niffler_tests.ui.pages.welcome_page import WelcomePage
from niffler_tests.utils.config import Config


class App:
    """Common Page object. It provides access to all the specified page objects.
    It is used to reduce the number of imports in the tests themselves.
    It can store methods that can be used across all the specified page objects."""

    URL = Config.app_url

    def __init__(self, page, user):
        self.username = user.get("name")
        self.password = user.get("password")
        self.page = page

        self.welcome_page = WelcomePage(page)
        self.login_page = LoginPage(page)
        self.main_page = MainPage(page)
        self.registration_page = RegistrationPage(page)

    def open(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_timeout(5000)

    def login(self):
        self.welcome_page.open(self.URL)
        self.welcome_page.click_login()
        self.login_page.fill_auth(self.username, self.password).click_login()
