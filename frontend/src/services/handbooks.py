from src.services.request_service import RequestService

BASE_PREFIX = "/handbooks"
CITIES_PREFIX = BASE_PREFIX + "/cities"
EXAMPLES_PREFIX = BASE_PREFIX + '/examples'


class HandbookService:

    @staticmethod
    def get_cities():
        response = RequestService.get(CITIES_PREFIX)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None

    @staticmethod
    def get_examples():
        response = RequestService.get(EXAMPLES_PREFIX)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None
