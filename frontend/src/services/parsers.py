from src.services.request_service import RequestService

BASE_PREFIX = "/parsers"

ORDER_PREFIX = BASE_PREFIX + "/orders"
AVAILABLE_PLATFORMS_MAPS_PREFIX = BASE_PREFIX + "/available_platforms/maps"
ORDERS_PREFIX = BASE_PREFIX + "/orders"
DETAIL_ORDER_PREFIX = BASE_PREFIX + "/orders/{}"


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

    @staticmethod
    def get_orders(x_token):
        response = RequestService.get_auth(ORDERS_PREFIX, x_token=x_token)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None

    @staticmethod
    def get_detail_by_id(order_id, x_token):
        response = RequestService.get_auth(DETAIL_ORDER_PREFIX.format(order_id), x_token=x_token)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None
