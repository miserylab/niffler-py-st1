from niffler_tests.ui.pages.component.header import Header
from niffler_tests.ui.pages.friends_page import FriendsPage
from niffler_tests.ui.pages.login_page import LoginPage
from niffler_tests.ui.pages.main_page import MainPage
from niffler_tests.ui.pages.people_page import PeoplePage
from niffler_tests.ui.pages.profile_page import ProfilePage
from niffler_tests.ui.pages.registration_page import RegistrationPage
from niffler_tests.ui.pages.welcome_page import WelcomePage
from niffler_tests.utils.config import Config


class App:
    """Common Page object. It provides access to all the specified page objects.
    It is used to reduce the number of imports in the tests themselves.
    It can store methods that can be used across all the specified page objects."""

    URL = Config.app_url

    def __init__(self, page, user):
        # self.username = user.get("name")
        # self.password = user.get("password")
        self.username = Config.username
        self.password = Config.password
        self.page = page

        self.welcome_page = WelcomePage(page)
        self.login_page = LoginPage(page)
        self.main_page = MainPage(page)
        self.registration_page = RegistrationPage(page)
        self.profile_page = ProfilePage(page)
        self.people_page = PeoplePage(page)
        self.header = Header(page)
        self.friends_page = FriendsPage(page)

    def open(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_timeout(5000)

    def login(self):
        self.welcome_page.open(self.URL)
        self.welcome_page.click_login()
        self.login_page.fill_auth(self.username, self.password).click_login()

    def _locator(self, locator: str):
        return self.page.locator(locator)

    def reload_page(self):
        self.page.reload()
