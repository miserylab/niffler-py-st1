import allure

from marks import Invitation, User
from niffler_tests.utils.config import Config


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Добавление в друзья")
@allure.tag("UI")
class TestFriendListPage:
    @allure.title("WEB: Пользователь может принять запрос в друзья на странице друзей")
    @User.get_token
    @Invitation.send({"username": Config.username})
    @User.logout_new_user
    @User.logout
    def test_submit_invite(self, get_token, send_invitation, app_url, app):
        _, username, _ = get_token

        app.welcome_page.open(app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(Config.username, Config.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_friends_page()
        app.friends_page.wait_for_page_loaded()

        app.friends_page.table.submit_and_decline_buttons_should_be_visible_after_invite(username)

        app.friends_page.table.submit_invite(username)

        app.friends_page.check_base_alert("Invitation is accepted")

        app.friends_page.table.check_actions_after_friend_submitted(username, "You are friends")

    @allure.title("WEB: Пользователь может отклонить запрос в друзья на странице друзей")
    @User.get_token
    @Invitation.send({"username": Config.username})
    @User.logout_new_user
    @User.logout
    def test_decline_invite(self, get_token, send_invitation, app_url, app):
        _, username, _ = get_token

        app.welcome_page.open(app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(Config.username, Config.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_friends_page()
        app.friends_page.wait_for_page_loaded()

        app.friends_page.table.submit_and_decline_buttons_should_be_visible_after_invite(username)

        app.friends_page.table.decline_invite(username)

        app.friends_page.check_base_alert("Invitation is declined")

        app.friends_page.table.username_should_not_be_present(username)

    @allure.title("WEB: Пользователь может удалить друга на странице друзей")
    @User.get_token
    @Invitation.send({"username": Config.username})
    @User.logout_new_user
    @User.logout
    def test_remove_friend(self, get_token, send_invitation, app_url, app):
        _, username, _ = get_token

        app.welcome_page.open(app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(Config.username, Config.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_friends_page()
        app.friends_page.wait_for_page_loaded()

        app.friends_page.table.submit_and_decline_buttons_should_be_visible_after_invite(username)

        app.friends_page.table.submit_invite(username)

        app.friends_page.check_base_alert("Invitation is accepted")

        app.friends_page.table.remove_friend(username)
        app.friends_page.check_base_alert("Friend is deleted")
        app.friends_page.table.username_should_not_be_present(username)
