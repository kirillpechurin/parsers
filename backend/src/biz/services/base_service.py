import os

import pymongo

from src.biz.exceptions.custom import InternalError


class BaseService:

    def __init__(self):
        try:
            self.client = pymongo.MongoClient(host="mongodb",
                                              port=27017,
                                              username=os.environ.get("MONGO_DB_USERNAME"),
                                              password=os.environ.get("MONGO_DB_PASSWORD"))
            self.db_name = self.client[os.environ.get("MONGO_DB_NAME")]
        except:
            raise InternalError
