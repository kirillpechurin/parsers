from src.biz.exceptions.custom import NotFoundError
from src.biz.services.base_service import BaseService

from src.biz.exceptions.enums import ExceptionEnum


class CityService(BaseService):

    def __init__(self):
        super(CityService, self).__init__()
        self.collection = self.db_name['cities']

    def get_cities(self):
        results = self.collection.find()
        results = [r['name'] for r in results if r]
        if not results:
            raise NotFoundError(ExceptionEnum.cities_not_found)
        return results
