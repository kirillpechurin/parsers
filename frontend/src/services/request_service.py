import json
import os

import requests

API_SERVER = "http://backend:8000/api/v1"
HEADER_TOKEN = "Authorization"
TOKEN = "Bearer {}"
ORIGIN_HEADER_VALUE = os.environ.get("ORIGIN")
ORIGIN_HEADER = "Origin"


class RequestService:

    @staticmethod
    def get(url, params=None):
        return requests.get(API_SERVER + url, params=params, headers={ORIGIN_HEADER: ORIGIN_HEADER_VALUE})

    @staticmethod
    def post(url, data=None):
        return requests.post(API_SERVER + url, data=json.dumps(data), headers={ORIGIN_HEADER: ORIGIN_HEADER_VALUE})

    @staticmethod
    def get_auth(url, x_token, params=None):
        return requests.get(API_SERVER + url, params=params, headers={HEADER_TOKEN: TOKEN.format(x_token),
                                                                      ORIGIN_HEADER: ORIGIN_HEADER_VALUE})

    @staticmethod
    def patch_auth(url, x_token, data):
        return requests.patch(API_SERVER + url, data=json.dumps(data), headers={HEADER_TOKEN: TOKEN.format(x_token),
                                                                                ORIGIN_HEADER: ORIGIN_HEADER_VALUE})

    @staticmethod
    def post_auth(url, x_token, data):
        return requests.post(API_SERVER + url, data=json.dumps(data), headers={HEADER_TOKEN: TOKEN.format(x_token),
                                                                               ORIGIN_HEADER: ORIGIN_HEADER_VALUE})

    @staticmethod
    def delete_auth(url, x_token):
        return requests.delete(API_SERVER + url, headers={HEADER_TOKEN: TOKEN.format(x_token),
                                                          ORIGIN_HEADER: ORIGIN_HEADER_VALUE})
