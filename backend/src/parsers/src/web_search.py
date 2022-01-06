import time

import selenium
from selenium.webdriver import Keys

from src.parsers.src.base_driver import BaseDriver


class WebSearch(BaseDriver):

    def __init__(self, driver, data: dict):
        super().__init__(driver)

        self.method_search_input = data['search_input']['method']
        self.value_search_input = data['search_input']['value']
        self.exception_method_search_input = data['search_input'].get("exception_method")
        self.exception_value_search_input = data['search_input'].get("exception_value")

        self.method_result_search = data['result_search']['method']
        self.value_result_search = data['result_search']['value']
        self.exception_method_result_search = data['result_search'].get("exception_method")
        self.exception_value_result_search = data['result_search'].get("exception_value")

    @staticmethod
    def find_need_href(result_search, sub_text):
        for item in result_search:
            if sub_text in item.text:
                return item
        return None

    def get_search_input(self):
        try:
            return self.find_one(self.method_search_input, self.value_search_input)
        except selenium.common.exceptions.NoSuchElementException as exc:
            print(exc.msg)
            if self.exception_method_search_input and self.exception_value_search_input:
                try:
                    return self.find_one(self.exception_method_search_input, self.exception_value_search_input)
                except selenium.common.exceptions.NoSuchElementException as exc:
                    print(exc.msg)
            return None

    def get_result_search(self):
        try:
            return self.find_list(self.method_result_search, self.value_result_search)
        except selenium.common.exceptions.NoSuchElementException as exc:
            print(exc.msg)
            if self.exception_method_result_search and self.exception_value_result_search:
                try:
                    return self.find_list(self.exception_method_result_search, self.exception_value_result_search)
                except selenium.common.exceptions.NoSuchElementException as exc:
                    print(exc.msg)
            return None

    def input_the_search(self, value):
        search_input = self.get_search_input()
        search_input.clear()
        search_input.send_keys(value)
        time.sleep(1)
        return self.get_result_search()

    def transition_to_branches(self, data: dict):
        """
        data example: {"city": "sub_text_city", "organisation": "sub_text_organisation"}
        :param data:
        :return:
        """
        for key, sub_text in data.items():
            result_search = self.input_the_search(key)
            href = self.find_need_href(result_search, sub_text)
            if href:
                self.click_element(href)
            else:
                search_input = self.get_search_input()
                search_input.send_keys(Keys.RETURN)
            self.sleep(3)
        return True
