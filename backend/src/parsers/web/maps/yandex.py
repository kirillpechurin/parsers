import functools
import os
import re
import uuid

from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys

from src.parsers.bs.maps.yandex import YandexParser
from src.parsers.src.middlewares import garbage_collector
from src.parsers.web.maps.interface import MapReviewsInterface
from src.parsers.src.base_reviews import BaseReviews

RESULT_SEARCH_CLASS_NAME = 'suggest-item-view__subtitle'  # Результаты при вводе текста в поисковый input
XPATH_HREF_ON_REVIEWS = "//div[@class='tabs-select-view__title _name_reviews']"  # xpath ссылка на отзывы
CLASS_NAME_INPUT_SEARCH = 'input__control'  # поисковый input

SOURCE_HTML_FILENAME = 'src/parsers/tmp/maps/source/source_yandex'  # общий файл для исходного html документа после прокрутки всех отзывов
RESULT_HTML_FILENAME = "src/parsers/results/maps/html/reviews_yandex"  # html file результатов парсинга

SEARCH_TEXT_CITY = "Россия"  # Вспомогательный текст для города
PATTERN_TEXT_COUNT_ORGANISATION = r'\d+ организаци'  # Вспомогательный текст для организации
CLASS_NAME_BRANCHES = 'search-snippet-view'  # div филиала
CLASS_NAME_HREF_ON_BRANCH = "search-snippet-view__link-overlay"  # ссылка на сам филиал в div филиала
XPATH_ADDRESS_ON_BRANCH = "//div[@class='business-contacts-view__address']"  # div адресса на странице филиала
CLASS_NAME_DIV_REVIEW = "business-reviews-card-view__review"  # div отзыва


class YandexReviews(BaseReviews, MapReviewsInterface):

    def __init__(self, driver: webdriver.Chrome, data: dict):
        super().__init__(driver, self.search_elements_data)
        self.url = "https://yandex.ru/maps/"

        self.result_filename = RESULT_HTML_FILENAME + str(uuid.uuid4()) + '.html'
        self.source_filename = SOURCE_HTML_FILENAME + str(uuid.uuid4()) + ".html"

        self.info_data = data
        self.info_data['map_name'] = "Yandex Maps"
        self.search_data = {
            data.get('city'): SEARCH_TEXT_CITY,
            data.get("organisation"): PATTERN_TEXT_COUNT_ORGANISATION
        }

        self.count_organisation = None
        self.set_implicitly_wait(self.driver, value=10)

    @property
    def search_elements_data(self):
        return {
            "search_input": {
                "method": "class_name",
                "value": CLASS_NAME_INPUT_SEARCH,
            },
            "result_search": {
                "method": "class_name",
                "value": RESULT_SEARCH_CLASS_NAME
            }
        }

    def __str__(self):
        return "yandex"

    @staticmethod
    def find_by_pattern(res, pattern):
        for item in res:
            result = re.search(pattern, item.text)
            if result:
                count_org = int(result.group().split()[0])
                need_href = item
                return count_org, need_href
        return None, None

    def transition_to_branches(self, data: dict):

        data_keys = list(data.keys())
        result_search = self.input_the_search(data_keys[0])
        href_city = self.find_need_href(result_search, data.get(data_keys[0]))
        if href_city:
            self.click_element(href_city)
        else:
            search_input = self.get_search_input()
            search_input.send_keys(Keys.RETURN)
        self.sleep(3)

        result_search = self.input_the_search(data_keys[1])
        count_organisation, href = self.find_by_pattern(result_search, data.get(data_keys[1]))
        if count_organisation or href:
            self.click_element(href)
        else:
            search_input = self.get_search_input()
            search_input.send_keys(Keys.RETURN)

        self.sleep(3)
        self.count_organisation = count_organisation
        return True

    def get_address(self):
        return self.find_one("xpath", XPATH_ADDRESS_ON_BRANCH).text

    def transition_to_reviews(self):
        href_review = self.find_one('xpath', XPATH_HREF_ON_REVIEWS)
        text_review = href_review.text
        self.click_element(href_review)
        return text_review

    def get_reviews(self):
        try:
            text_review = self.transition_to_reviews()
        except NoSuchElementException as exc:
            print(exc.msg)
            return []
        count_reviews = int(re.search(r'\d+$', text_review).group())

        return self._get_reviews(count_reviews=count_reviews,
                                 accordance_method="class_name",
                                 accordance_exp=CLASS_NAME_DIV_REVIEW,
                                 filename=self.source_filename,
                                 instance_parser=YandexParser
                                 )

    def get_links_on_branches(self, count_elements):
        branches = self.get_accordance('class_name', CLASS_NAME_BRANCHES, count_elements=count_elements)
        return [
            item.find_element_by_class_name(CLASS_NAME_HREF_ON_BRANCH).get_attribute('href') for item in branches
        ]

    def get_reviews_by_links(self, links):
        all_reviews = {}
        for link in links:
            self.driver.get(link)
            self.sleep(3)
            address = self.get_address()
            reviews = self.get_reviews()

            if all_reviews.get(address):
                all_reviews[address].extend(reviews)
            else:
                all_reviews[address] = reviews
        return all_reviews

    @garbage_collector
    def find(self):
        self.driver.get(self.url)
        self.sleep(5)
        result = self.transition_to_branches(self.search_data)
        if not result:
            return None

        links = self.get_links_on_branches(self.count_organisation)
        all_reviews = self.get_reviews_by_links(links)

        html_filename = self.render_html(self.result_filename, all_reviews, self.info_data)
        return all_reviews, html_filename


if __name__ == '__main__':
    start = datetime.now()
    wd = webdriver.Firefox(executable_path='/geckodriver')
    YandexReviews(
        driver=wd,
        data={"city": "Пермь", "organisation": "Лион"}
    ).find()
    print(datetime.now() - start)
