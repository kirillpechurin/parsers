from src.services.request_service import RequestService

SIGNUP_PREFIX = "/auth/signup"
LOGIN_PREFIX = "/auth/login"


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