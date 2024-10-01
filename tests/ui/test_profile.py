import allure
import pytest


@allure.epic("Frontend")
@allure.feature("Niffler")
@allure.story("Профиль")
@allure.tag("UI")
class TestProfilePage:
    @pytest.mark.usefixtures("register_new_user_and_login")
    @allure.title("WEB: Пользователь может отредактировать все поля в профиле")
    def test_update_user_profile_all_fields(self, app, test_data):
        data = test_data["profile_all_fields_data"]
        app.profile_page.open()
        app.profile_page.wait_for_page_loaded()
        app.profile_page.set_name(data["name"])
        app.profile_page.set_surname(data["surname"])
        app.profile_page.set_currency(data["currency"])
        app.profile_page.submit_profile()
        app.profile_page.check_base_alert("Profile successfully updated")

        app.page.reload()

        app.profile_page.check_name(data["name"])
        app.profile_page.check_surname(data["surname"])
        app.profile_page.check_currency(data["currency"])

    @pytest.mark.usefixtures("register_new_user_and_login", "logout")
    @allure.title("WEB: Пользователь может отредактировать профиль с заполнением только обязательных полей")
    def test_update_user_profile_required_field_only(self, app):
        app.profile_page.open()
        app.profile_page.wait_for_page_loaded()
        app.profile_page.set_currency("KZT")
        app.profile_page.submit_profile()
        app.profile_page.check_base_alert("Profile successfully updated")

        app.page.reload()

        app.profile_page.check_name("")
        app.profile_page.check_surname("")
        app.profile_page.check_currency("KZT")

    @pytest.mark.usefixtures("register_new_user_and_login", "logout")
    @allure.title("WEB: Пользователь имеет возможность добавить категорию трат")
    def test_add_new_category(self, app, test_data):
        data = test_data["category_data"]
        app.profile_page.open()
        app.profile_page.wait_for_page_loaded()
        app.profile_page.add_category(data["name"])
        app.profile_page.check_base_alert("New category added")

        app.page.reload()

        app.profile_page.check_category_exists(data["name"])

    @pytest.mark.usefixtures("register_new_user_and_login", "logout")
    @allure.title("WEB: Пользователь не имеет возможности добавить более 8 трат")
    def test_add_more_than_8_not_allowed(self, app, test_data):
        TEST_CATEGORIES = ["Food", "Bars", "Clothes", "Music", "Sports", "Walks", "Books", "Travel"]
        data = test_data["category_data"]
        app.profile_page.open()
        app.profile_page.wait_for_page_loaded()

        for category in TEST_CATEGORIES:
            app.profile_page.add_category(category)
            app.profile_page.check_base_alert("New category added")

        app.profile_page.add_category(data["name"])
        app.profile_page.check_base_alert("Can not add new category")
