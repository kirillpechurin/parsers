from abc import ABC
from selenium import webdriver
from src.parsers.output.html.maps import RenderHTMLBody
from src.parsers.src.ajax_handling import AjaxHandling
from src.parsers.src.base_driver import BaseDriver
from src.parsers.src.web_search import WebSearch


class BaseReviews(BaseDriver, ABC):

    def __init__(self,
                 driver: webdriver,
                 search_elements_data: dict):
        super().__init__(driver=driver)
        self.ajax_handling = AjaxHandling(self.driver)
        self.web_search = WebSearch(self.driver, search_elements_data)

    def do_scroll_to_element(self, element):
        return self.ajax_handling.scroll.do_scroll_to_elem(element)

    def get_accordance(self, method_search, value_search, count_elements):
        return self.ajax_handling.get_accordance(method_search, value_search, count_elements)

    @staticmethod
    def render_html(filename, reviews):
        return RenderHTMLBody(filename).create(reviews)

    def _get_reviews(self,
                     count_reviews,
                     accordance_method,
                     accordance_exp,
                     filename,
                     instance_parser):
        self.get_accordance(accordance_method, accordance_exp, count_reviews)

        with open(filename, mode='w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

        return instance_parser(filename).parsing()

    def transition_to_branches(self, data: dict):
        return self.web_search.transition_to_branches(data)

    def find_need_href(self, results, sub_text):
        return self.web_search.find_need_href(results, sub_text)

    def input_the_search(self, value):
        return self.web_search.input_the_search(value)

    def get_search_input(self):
        return self.web_search.get_search_input()
