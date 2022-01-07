from app.models.parsers import Map
from src.biz.exceptions.custom import NotFoundError
from src.biz.services.base_service import BaseService

from src.biz.exceptions.enums import ExceptionEnum


class MapService(BaseService):

    def __init__(self):
        super(MapService, self).__init__()
        self.collection = self.db_name['maps']

    def get_available_maps(self):
        results = self.collection.find({"available": True})
        results = [r for r in results]
        if not results:
            raise NotFoundError(ExceptionEnum.maps_not_found)
        data = []
        for result in results:
            data.append(
                Map.parse_obj(result)
            )
        return data
