import pymongo


class BaseService:

    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost",
                                          port=27017,
                                          username="kirill",
                                          password="k1979082002")
        self.db_name = self.client['parsers_db']
