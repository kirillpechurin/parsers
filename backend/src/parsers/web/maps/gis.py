import re
import uuid
from datetime import datetime

from selenium import webdriver

from src.parsers.bs.maps.gis import GisParser
from src.parsers.src.middlewares import garbage_collector
from src.parsers.web.maps.interface import MapReviewsInterface
from src.parsers.src.base_reviews import BaseReviews

BRANCHES_CLASS_NAME = '_1hf7139'  # класс div филиалов
ALL_BRANCHES_CLASS_NAME = '_120g3oa'  # класс div при выборе филиала, где вкладка "Все филиалы"
DIV_WITH_DOP_INFO_BY_ORG = '_1p8iqzw'  # [сеть супермаркетов, 217 филиалов организации]
HREF_CLASS_NAME = '_1kmhi0c'  # ссылка
REVIEWS_CLASS_NAME = '_11gvyqv'  # class name для отзывов. Это div отзыва
CLASS_NAME_SEARCH_INPUT = "_1gvu1zk"  # Первый div для поискового inputa
CLASS_NAME_SEARCH_INPUT_FULL = "_1dhzhec9"  # Второй div для поискового inputa (динамическое изменение при наведении)
CLASS_NAME_SEARCH_RESULTS = "_1vsscbe"  # Результаты при вводе текста в поисковый input
TEXT_REVIEWS = r'Отзывы'  # вспомогательный текст чтобы найти нужную ссылку

SOURCE_HTML_FILENAME = 'src/parsers/tmp/maps/source/source_gis'  # общий файл для исходного html документа после прокрутки всех отзывов
RESULT_HTML_FILENAME = "src/parsers/results/maps/html/reviews_gis"  # html file результатов парсинга


class GisReviews(BaseReviews, MapReviewsInterface):

    def __init__(self, driver: webdriver.Chrome, data: dict):
        super().__init__(driver, self.search_elements_data)
        self.search_data = {
            data.get("city"): data.get("city"),
            data.get("organisation"): data.get("organisation")
        }
        self.url = "https://2gis.ru/"

        self.result_filename = RESULT_HTML_FILENAME + str(uuid.uuid4()) + '.html'
        self.source_filename = SOURCE_HTML_FILENAME + str(uuid.uuid4()) + ".html"

        self.set_implicitly_wait(self.driver, value=10)

    @property
    def search_elements_data(self):
        return {
            "search_input": {
                "method": "class_name",
                "value": CLASS_NAME_SEARCH_INPUT,
                "exception_method": "class_name",
                "exception_value": CLASS_NAME_SEARCH_INPUT_FULL
            },
            "result_search": {
                "method": "class_name",
                "value": CLASS_NAME_SEARCH_RESULTS
            }
        }

    def __str__(self):
        return "gis"

    def get_reviews(self):
        text_review = self.transition_to_reviews()
        count_reviews = int(re.search(r'\d+$', text_review).group())

        return self._get_reviews(
            count_reviews=count_reviews,
            accordance_method="class_name",
            accordance_exp=REVIEWS_CLASS_NAME,
            filename=self.source_filename,
            instance_parser=GisParser
        )

    def transition_to_reviews(self):
        branch = self.find_one('class_name', BRANCHES_CLASS_NAME)
        self.click_element(branch)

        hrefs = self.find_list('class_name', HREF_CLASS_NAME)
        href_review = self.find_need_href(hrefs, TEXT_REVIEWS)
        self.click_element(href_review)

        all_branches_link = self.find_one('class_name', ALL_BRANCHES_CLASS_NAME)
        self.click_element(all_branches_link)

        href_review = self.find_need_href(hrefs, TEXT_REVIEWS)
        text_review = href_review.text
        return text_review

    @garbage_collector
    def find(self):
        self.driver.get(self.url)
        result = self.transition_to_branches(self.search_data)
        if not result:
            return None, None
        reviews = self.get_reviews()
        html_filename = self.render_html(self.result_filename, reviews)
        return reviews, html_filename


if __name__ == '__main__':
    start = datetime.now()
    wd = webdriver.Firefox(executable_path='/geckodriver')
    GisReviews(
        driver=wd,
        data={"city": "Пермь", "organisation": "Digital spectr"}
    ).find()
    print(datetime.now() - start)

