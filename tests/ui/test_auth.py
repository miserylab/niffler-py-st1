# import allure
# import pytest
# import requests
#
# from niffler_tests.utils.auth.auth_api_client import AuthApiClient
# from niffler_tests.utils.config import Config
# from niffler_tests.utils.utils import Utils
#
#
# @allure.epic("Frontend")
# @allure.feature("Niffler")
# @allure.story("Аутентификация")
# @allure.tag("UI")
# class TestAuth:
#     # TODO переделать, чтобы работало
#     def test_auth2(self, app):
#         client = AuthApiClient(auth_url=Config.auth_url, front_url=Config.app_url)
#         access_token = client.do_login(Config.username, Config.password)
#         print(f"Access Token: {access_token}")
#
#     def test_auth(app):
#         # Create a session instance
#         session = requests.Session()
#
#         code_verifier = Utils.generate_code_verifier()
#         code_challenge = Utils.generate_code_challenge(code_verifier)
#
#         # Use the session instance to make the request
#         response = session.get(
#             f"{Config.auth_url}/oauth2/authorize",
#             params={
#                 "response_type": "code",
#                 "client_id": "client",
#                 "scope": "openid",
#                 "redirect_uri": Config.app_url + "/authorized",
#                 "code_challenge": code_challenge,
#                 "code_challenge_method": "S256"
#             }
#         )
#
#         print(response.request.hooks)
#
#         # Extract XSRF-TOKEN from the session's cookies
#         xsrf_token = session.cookies.get('XSRF-TOKEN')
#         print(xsrf_token)
#
#         # Use the session to post login data
#         response_login = session.post(
#             "http://auth.niffler.dc:9000/login",
#             data={
#                 "_csrf": xsrf_token,
#                 "username": Config.username,
#                 "password": Config.password
#             },
#             headers={
#                 "Content-Type": "application/x-www-form-urlencoded"
#             }, verify=False
#         )
#         print(response_login.cookies)
#         print(response_login.headers)
#         print(response_login.url)
#         print(response_login.status_code)
#         user_code = response_login.url[response_login.url.find("?code=") + len("?code="):]
#         print(f"user_code : {user_code}")
#
#         # return user_code
#
#     # http://frontend.niffler.dc/authorized?code=DV9-V1tbBSA46Ccg0Yeb0B82Y0rISz2nn66D7MtuK_LjWB00hrzyyQTmdqemba-22-pTvvctPWscxEpWkCtDZgbMF0LrLEFZ1oGAuwFTjxeO769rQIHYPS-2GzyfEj0s
#     # response_1 = session.get(
#     #     f"{Config.app_url}/authorized?code={code}"
#     # )
#     # print(response_1)
#     #
#     # url = f"{Config.auth_url}/oauth2/token"
#     # data = {
#     #     "code": code,
#     #     "redirect_uri": Config.app_url + "/authorized",
#     #     "code_verifier": code_verifier,
#     #     "grant_type": "authorization_code",
#     #     "client_id": "client"
#     # }
#     # headers = {
#     #     "Content-Type": "application/x-www-form-urlencoded"
#     # }
#     # response = requests.post(url, data=data, headers=headers)
#     # print(response)
#     # pass
#
#     @pytest.mark.usefixtures("get_token")
#     def test_profile(self, app):
#         print(app.page.url)
