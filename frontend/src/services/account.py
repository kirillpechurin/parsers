from src.services.request_service import RequestService

SIGNUP_PREFIX = "/auth/signup"
LOGIN_PREFIX = "/auth/login"
CHECK_TOKEN_PREFIX = "/auth/check_token"


class AccountService:

    @staticmethod
    def signup(data):
        response = RequestService.post(SIGNUP_PREFIX, data=data)
        if response.status_code != 201:
            return None, response.json()['detail']
        return response.json()['data'], None

    @staticmethod
    def login(data):
        response = RequestService.post(LOGIN_PREFIX, data=data)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None

    @staticmethod
    def check_token(data):
        response = RequestService.post(CHECK_TOKEN_PREFIX, data=data)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None

    @staticmethod
    def confirm_email(account_id):
        response = RequestService.post(f"/auth/confirm/{account_id}")
        if response.status_code != 204:
            return None, response.json()['detail']
        return None, None
