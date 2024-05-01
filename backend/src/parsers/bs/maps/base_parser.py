from bs4 import BeautifulSoup


class BaseParser:

    def __init__(self, filename):
        self.filename = filename
        self._reviews = None
        with open(filename, mode='r', encoding='utf-8') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')

    @property
    def reviews(self):
        if not self._reviews:
            self._reviews = self.parsing()
        return self._reviews

    def parsing(self):
        raise NotImplementedError
