import argparse

from src.biz.services.base_service import BaseService
from src.utils.work_json_file import WorkJsonFile


class Command:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Load data parser")
        self.db = BaseService().db_name
        self.set_arguments()

    def set_arguments(self):
        self.parser.add_argument(
            "filename",
            type=str,
            help="json filename"
        )

    def start(self):
        args = self.parser.parse_args()
        data: dict = WorkJsonFile(filename=args.filename).read()
        for key, values in data.items():
            collection = self.db[key]
            for value in values:
                result = collection.find_one(value)
                if result:
                    print("Duplicate data in collection: {}.".format(collection.name))
                else:
                    collection.insert_one(value)
        print("Success upload init data")


def start_command():
    command = Command()
    command.start()
