import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page_fixture")


class User:
    login = pytest.mark.usefixtures("auth")
    generate = pytest.mark.usefixtures("register_new_user_and_login")
    get_token = pytest.mark.usefixtures("get_token")
    logout_new_user = pytest.mark.usefixtures("logout_user")
    logout = pytest.mark.usefixtures("ui_logout")
    delete_user_with_friendship = pytest.mark.usefixtures("delete_user_with_friendship")
    delete_user_wo_friendship = pytest.mark.usefixtures("delete_user_wo_friendship")



class Invitation:
    send = lambda x: pytest.mark.parametrize("send_invitation", [x], indirect=True)


class GenerateData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param.description)


class Actions:
    delete_all_spendings = pytest.mark.usefixtures("api_delete_all_spendings")