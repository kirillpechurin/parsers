from src.biz.exceptions.custom import NotFoundError
from src.biz.services.base_service import BaseService


class CityService(BaseService):

    def __init__(self):
        super(CityService, self).__init__()
        self.collection = self.db_name['cities']

    def get_cities(self):
        results = self.collection.find()
        results = [r['name'] for r in results if r]
        if not results:
            raise NotFoundError("Cities not found")
        return results
