import json

import requests

API_SERVER = "http://localhost:8000"
HEADER_TOKEN = "Authorization"
TOKEN = "Bearer {}"


class RequestService:

    @staticmethod
    def post(url, data=None):
        return requests.post(API_SERVER + url, data=json.dumps(data))
