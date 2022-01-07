import json


class WorkJsonFile:

    def __init__(self, filename: str):
        self.filename = filename
        self.ensure_ascii = False
        self.sort_keys = True
        self.indent = 4

    def write(self, data, mode="w"):
        with open(self.filename, mode=mode, encoding='utf-8') as file:
            json.dump(
                data,
                file,
                ensure_ascii=self.ensure_ascii,
                sort_keys=self.sort_keys,
                indent=self.indent
            )

    def append(self, data, mode='r+'):
        with open(self.filename, mode=mode) as file:
            info_in_file = json.load(file)
            if isinstance(data, list):
                for item in data:
                    info_in_file.append(item)
            else:
                info_in_file.append(data)
            file.seek(0)
            json.dump(
                info_in_file,
                file,
                ensure_ascii=self.ensure_ascii,
                sort_keys=self.sort_keys,
                indent=self.indent
            )

    def initialize(self, data, mode="w"):
        with open(self.filename, mode=mode) as f:
            json.dump(
                data,
                f,
                ensure_ascii=self.ensure_ascii,
                sort_keys=self.sort_keys,
                indent=self.indent
            )

    def read(self, mode="r"):
        with open(self.filename, mode=mode) as f:
            return json.load(f)
