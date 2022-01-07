from src.services.request_service import RequestService

BASE_PREFIX = "/handbooks"
CITIES_PREFIX = BASE_PREFIX + "/cities"


class HandbookService:

    @staticmethod
    def get_cities():
        response = RequestService.get(CITIES_PREFIX)
        if response.status_code != 200:
            return None, response.json()['detail']
        return response.json()['data'], None
