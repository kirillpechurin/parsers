from src.biz.exceptions.custom import NotFoundError
from src.biz.services.base_service import BaseService

from src.biz.exceptions.enums import ExceptionEnum


class ExampleService(BaseService):

    def __init__(self):
        super(ExampleService, self).__init__()
        self.collection = self.db_name['examples']

    def get_maps_examples(self):
        result = self.collection.find_one({"type": "maps"})
        if not result:
            raise NotFoundError(ExceptionEnum.maps_examples_not_found)
        return result['examples']
