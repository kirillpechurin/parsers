from src.utils.work_json_file import WorkJsonFile


class JsonFile:

    def __init__(self, filename):
        self.filename = filename

    def create(self, reviews: dict, info_data: dict):
        content = {
            "meta": info_data,
            "data": reviews
        }
        WorkJsonFile(filename=self.filename).write(data=content)
        return self.filename
