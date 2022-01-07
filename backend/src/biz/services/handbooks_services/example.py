from src.biz.exceptions.custom import NotFoundError
from src.biz.services.base_service import BaseService


class ExampleService(BaseService):

    def __init__(self):
        super(ExampleService, self).__init__()
        self.collection = self.db_name['examples']

    def get_maps_examples(self):
        result = self.collection.find_one({"type": "maps"})
        if not result:
            raise NotFoundError("Maps examples not found")
        return result['examples']
