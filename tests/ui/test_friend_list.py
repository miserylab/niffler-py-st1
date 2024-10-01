import allure
import pytest

from niffler_tests.utils.config import Config


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Добавление в друзья")
@allure.tag("UI")
class TestFriendListPage:
    @pytest.mark.usefixtures("logout")
    def test_add_friend_on_people_page(self, app_url, app, register_new_user):
        username, _, _ = register_new_user

        app.welcome_page.open(app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(Config.username, Config.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.people_page.open()
        app.people_page.wait_for_page_loaded()

        app.people_page.people_table.add_friend(username)
        app.people_page.check_base_alert("Invitation is sent")
        app.people_page.people_table.check_add_button(username, "Pending invitation")
