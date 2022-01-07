import json

import requests

API_SERVER = "http://backend:8000"
HEADER_TOKEN = "Authorization"
TOKEN = "Bearer {}"


class RequestService:

    @staticmethod
    def post(url, data=None):
        return requests.post(API_SERVER + url, data=json.dumps(data))

    @staticmethod
    def get_auth(url, x_token, params=None):
        return requests.get(API_SERVER + url, params=params, headers={HEADER_TOKEN: TOKEN.format(x_token)})
