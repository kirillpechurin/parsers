from src.services.request_service import RequestService

SIGNUP_PREFIX = "/auth/signup"
LOGIN_PREFIX = "/auth/login"
CHECK_TOKEN_PREFIX = "/auth/check_token"
CONFIRM_ACCOUNT_PREFIX = "/auth/confirm/{}"
FORGOT_PASSWORD_PREFIX = "/auth/password/forgot"
RESET_PASSWORD_PREFIX = "/auth/password/reset/{}"
ACCOUNT_DETAIL_PREFIX = "/auth/me"
UPDATE_ACCOUNT_PREFIX = '/auth/me/update'
RESET_PASSWORD_AUTH_PREFIX = '/auth/password/reset/auth'


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
        response = RequestService.post(CONFIRM_ACCOUNT_PREFIX.format(account_id))
        if response.status_code != 204:
            return None, response.json()['detail']
        return None, None

    @staticmethod
    def forgot_password(data):
        response = RequestService.post(FORGOT_PASSWORD_PREFIX, data=data)
        if response.status_code != 204:
            return None, response.json()['detail']
        return None, None

    @staticmethod
    def reset_password(account_id, data):
        response = RequestService.post(RESET_PASSWORD_PREFIX.format(account_id), data=data)
        if response.status_code != 204:
            return None, response.json()['detail']
        return None, None

    @staticmethod
    def get_detail(x_token):
        response = RequestService.get_auth(ACCOUNT_DETAIL_PREFIX, x_token)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None

    @staticmethod
    def update_account(data, x_token):
        response = RequestService.patch_auth(UPDATE_ACCOUNT_PREFIX, data=data, x_token=x_token)
        if response.status_code != 204:
            return None, response.json()['detail']
        return None, None

    @staticmethod
    def update_password(data, x_token):
        response = RequestService.post_auth(RESET_PASSWORD_AUTH_PREFIX, data=data, x_token=x_token)
        if response.status_code != 204:
            return None, response.json()['detail']
        return None, None
