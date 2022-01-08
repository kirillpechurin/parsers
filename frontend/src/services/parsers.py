from src.services.request_service import RequestService

BASE_PREFIX = "/parsers"

ORDER_PREFIX = BASE_PREFIX + "/orders"
AVAILABLE_PLATFORMS_MAPS_PREFIX = BASE_PREFIX + "/available_platforms/maps"


class ParserService:

    @staticmethod
    def get_available_platforms(x_token):
        response = RequestService.get_auth(AVAILABLE_PLATFORMS_MAPS_PREFIX, x_token=x_token)
        if response.status_code != 200:
            return None, response.json()['detail']
        return {'maps': response.json()['data']}, None

    @staticmethod
    def make_order(x_token, data):
        response = RequestService.post_auth(ORDER_PREFIX, data=data, x_token=x_token)
        if response.status_code != 201:
            return None, response.json()['detail']
        return response.json()['data'], None
