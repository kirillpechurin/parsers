import re
import uuid
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import Keys

from src.parsers.bs.maps.google import GoogleParser
from src.parsers.src.middlewares import garbage_collector
from src.parsers.web.maps.interface import MapReviewsInterface
from src.parsers.src.base_reviews import BaseReviews

TEXT_FOR_SEARCH_INPUT_ORGANISATION = "Посмотреть адреса"  # По этому тексту можно определить нужную ссылку для результатов
XPATH_BUTTON_NEXT = "//button[@id='ppdPk-Ej1Yeb-LgbsSe-tJiF1e']"  # Кнопка на следующие 20 результатов
ATTRIBUTE_DISABLED_BUTTON = "disabled"  # Атрибут. Пристуствует если кнопка на следующие 20 результатов отключена
XPATH_INTERMEDIATE_BRANCHES = "//div[@class='TFQHme']"  # Есть пустой div между филиалами, его считаем. С подсчётом филиалов трудно
XPATH_LINK_ON_BRANCH = "//a[@class='a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd']"  # Ссылка <a> на филиал
XPATH_GENERAL_DIV = "//div[@class='x3AX1-LfntMc-header-title']"  # Общий div, где находится название, отзывы, оценка на странице филиала

XPATH_GENERAL_GRADE = "//span[@class='aMPvhf-fI6EEc-KVuj8d']"  # Общая оценка филиала
XPATH_GENERAL_STAR = "//li[@class='section-star']"  # Общая оценка в звездочках
XPATH_HREF_ON_REVIEWS = "//button[@class='Yr7JMd-pane-hSRGPd']"  # Ссылка на отзывы с текстом "123 отзыва"
CLASS_NAME_REVIEW = 'ODSEW-ShBeI'  # класс div отзыва

XPATH_GENERAL_DIV_ALL_BRANCHES = "//div[@class='siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc siAUzd-neVct-Q3DXx-BvBYQ']"  # общий div, где отображаются все филиалы
TEXT_FOR_CHECK_RESULTS = "Ничего не найдено"  # Текст, по которому можно определить, есть ли результаты на странице

SOURCE_FILENAME = 'src/parsers/tmp/maps/source/source_google'  # общий файл для исходного html документа после прокрутки всех отзывов
RESULT_FILENAME = "src/parsers/results/maps/html/reviews_google"  # html file результатов парсинга

CLASS_NAME_RESULTS_SEARCH = 'sbsb_c'  # класс результатов поиска
CLASS_NAME_SEARCH_INPUT = 'tactile-searchbox-input'  # класс div поиска
CLASS_NAME_COUNT_RESULTS_IN_PAGE = 'Jl2AFb'  # класс div количество результатов на странице


class GoogleReviews(BaseReviews, MapReviewsInterface):

    def __init__(self, driver: webdriver.Chrome, data: dict):
        super().__init__(driver, self.search_elements_data)

        self.url = 'https://www.google.ru/maps/'

        result_filename = RESULT_FILENAME + str(uuid.uuid4())
        self.result_html_filename = result_filename + '.html'
        self.result_json_filename = result_filename + ".json"
        self.source_filename = SOURCE_FILENAME + str(uuid.uuid4()) + ".html"

        self.search_data = {
            data.get("city"): data.get("city"),
            data.get("organisation"): TEXT_FOR_SEARCH_INPUT_ORGANISATION
        }

        self.info_data = data
        self.info_data['map_name'] = "Google Maps"

        self.set_implicitly_wait(self.driver, value=10)

    @property
    def search_elements_data(self):
        return {
            "search_input": {
                "method": "class_name",
                "value": CLASS_NAME_SEARCH_INPUT,
            },
            "result_search": {
                "method": "class_name",
                "value": CLASS_NAME_RESULTS_SEARCH
            }
        }

    def __str__(self):
        return "google"

    def count_result_in_page(self):
        count_result = self.find_one('class_name', CLASS_NAME_COUNT_RESULTS_IN_PAGE)
        res_re_search = re.findall(r'\d+', count_result.text)
        if not res_re_search:
            return None, None
        return map(int, res_re_search)

    def check_next_page(self):
        check_results = self.find_one(
            "xpath",
            XPATH_GENERAL_DIV_ALL_BRANCHES
        )
        if TEXT_FOR_CHECK_RESULTS in check_results.text:
            return False
        return True

    def check_branch_on_reviews(self):
        general_div = self.find_one("xpath", XPATH_GENERAL_DIV)
        if "отзыв" not in general_div.text:
            return False
        return True

    def get_address(self):
        return self.find_one("xpath", "//div[@class='rogA2c']").text

    def transition_to_reviews(self):
        href_review = self.find_one("xpath", XPATH_HREF_ON_REVIEWS)
        text_review = href_review.text
        self.click_element(href_review)
        return text_review

    def get_reviews(self):
        if not self.check_branch_on_reviews():
            return None

        text_review = self.transition_to_reviews()
        list_str_digit = re.findall(r"\d+", text_review)
        count_reviews = int("".join(list_str_digit))

        return self._get_reviews(count_reviews=count_reviews,
                                 accordance_method="class_name",
                                 accordance_exp=CLASS_NAME_REVIEW,
                                 filename=self.source_filename,
                                 instance_parser=GoogleParser)

    def get_reviews_by_links(self, links):
        all_reviews = {}
        for link in links:
            self.driver.get(link)
            self.sleep(3)
            address = self.get_address()
            reviews = self.get_reviews()
            if not reviews:
                reviews = []
            if all_reviews.get(address):
                all_reviews[address].extend(reviews)
            else:
                all_reviews[address] = reviews

        return all_reviews

    def transition_to_next_page(self, button_next):
        self.click_element(button_next)
        if not self.check_next_page():
            print("Results is over!")
            return False
        self.sleep(3)
        return True

    def get_links_on_branches(self, count_elements):
        self.get_accordance("xpath", XPATH_INTERMEDIATE_BRANCHES, count_elements)
        branches = self.find_list("xpath", XPATH_LINK_ON_BRANCH)
        return [branch.get_attribute("href") for branch in branches]

    def find_by_pages(self):
        all_reviews = {}
        first_value = None
        self.sleep(3)
        main_url = self.driver.current_url
        checklist = []

        button_next = self.find_one('xpath', XPATH_BUTTON_NEXT)
        check_first_value, check_second_value = self.count_result_in_page()
        while ATTRIBUTE_DISABLED_BUTTON not in button_next.get_attribute("class") or check_second_value < 20:
            check_second_value = 21
            if first_value:
                res = self.transition_to_next_page(button_next)
                if not res:
                    break

            first_value, second_value = self.count_result_in_page()
            if not first_value and not second_value:
                break

            if (first_value, second_value) not in checklist:
                print("{} : {}".format(first_value, second_value))
                checklist.append((first_value, second_value))

                links = self.get_links_on_branches(second_value - first_value)
                reviews = self.get_reviews_by_links(links)

                all_reviews.update(reviews)

                self.driver.get(main_url)
                self.sleep(2)

            button_next = self.find_one('xpath', XPATH_BUTTON_NEXT)
        return all_reviews

    @garbage_collector
    def find(self):
        self.driver.get(self.url)
        result = self.transition_to_branches(self.search_data)
        if not result:
            return None, None
        reviews = self.find_by_pages()
        html_filename = self.render_html(self.result_html_filename, reviews, self.info_data)
        json_filename = self.create_json(self.result_json_filename, reviews, self.info_data)
        return reviews, html_filename, json_filename
