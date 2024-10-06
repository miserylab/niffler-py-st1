import allure

from marks import Invitation, User
from niffler_tests.utils.config import Config


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("People")
@allure.tag("UI")
class TestPeopleListPage:
    @allure.title("WEB: Пользователь может принять запрос в друзья на странице со списком всех пользователей")
    @User.get_token
    @Invitation.send({"username": Config.username})
    @User.logout_new_user
    @User.logout
    @User.delete_user_with_friendship
    def test_submit_invite(self, get_token, send_invitation, envs, app):
        _, username, _ = get_token

        app.welcome_page.open(envs.app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(envs.username, envs.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_people_page()
        app.people_page.wait_for_page_loaded()

        app.people_page.table.submit_and_decline_buttons_should_be_visible_after_invite(username)

        app.people_page.table.submit_invite(username)

        app.people_page.check_base_alert("Invitation is accepted")

        app.people_page.table.check_actions_after_friend_submitted(username, "You are friends")

    @allure.title("WEB: Пользователь может отклонить запрос в друзья на странице со списком всех пользователей")
    @User.get_token
    @Invitation.send({"username": Config.username})
    @User.logout_new_user
    @User.logout
    @User.delete_user_wo_friendship
    def test_decline_invite(self, get_token, send_invitation, envs, app):
        _, username, _ = get_token

        app.welcome_page.open(envs.app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(envs.username, envs.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_people_page()
        app.people_page.wait_for_page_loaded()

        app.people_page.table.submit_and_decline_buttons_should_be_visible_after_invite(username)

        app.people_page.table.decline_invite(username)

        app.people_page.check_base_alert("Invitation is declined")

        app.people_page.table.check_actions_after_friend_declined(username)

    @allure.title("WEB: Пользователь может отправить запрос в друзья на странице со списком всех пользователей")
    @User.logout
    def test_send_friend_request(self, envs, app, register_new_user):
        username, _, _ = register_new_user

        app.welcome_page.open(envs.app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(envs.username, envs.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_people_page()
        app.people_page.wait_for_page_loaded()

        app.people_page.table.add_friend(username)
        app.people_page.check_base_alert("Invitation is sent")
        app.people_page.table.check_add_button(username, "Pending invitation")

    @allure.title("WEB: Пользователь может удалить друга на странице со списком всех пользователей")
    @User.get_token
    @Invitation.send({"username": Config.username})
    @User.logout_new_user
    @User.logout
    @User.delete_user_wo_friendship
    def test_remove_friend(self, get_token, send_invitation, envs, app):
        _, username, _ = get_token

        app.welcome_page.open(envs.app_url)
        app.welcome_page.click_login()
        app.login_page.fill_auth(envs.username, envs.password).click_login()
        app.page.wait_for_load_state("networkidle")
        app.main_page.wait_for_page_loaded()

        app.main_page.header.to_people_page()
        app.people_page.wait_for_page_loaded()

        app.people_page.table.submit_and_decline_buttons_should_be_visible_after_invite(username)

        app.people_page.table.submit_invite(username)

        app.people_page.check_base_alert("Invitation is accepted")

        app.people_page.table.remove_friend(username)
        app.people_page.check_base_alert("Friend is deleted")
        app.people_page.table.check_actions_after_friend_removed(username)
