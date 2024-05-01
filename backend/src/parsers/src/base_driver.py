import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from src.parsers.src.const import DEFAULT_TIME_SLEEP
from src.parsers.src.my_driver import Driver
from src.parsers.src.search_methods import SearchMethods


class BaseDriver(Driver):

    def __init__(self,
                 driver: webdriver.Firefox):
        super().__init__(driver)
        self.search_methods = SearchMethods(self.driver)

    def find_list(self, method, value):
        return self.search_methods.find_list(method, value)

    def find_one(self, method, value):
        return self.search_methods.find_one(method, value)

    def find_one_at_object(self, obj, method, value):
        return self.search_methods.find_one_at_object(obj, method, value)

    def find_list_at_object(self, obj, method, value):
        return self.search_methods.find_list_at_object(obj, method, value)

    def input_the_form(self, need_input, value):
        need_input.clear()
        need_input.send_keys(value)
        self.sleep(DEFAULT_TIME_SLEEP)

    def click_element(self, elem):
        try:
            elem.click()
        except selenium.common.exceptions.ElementClickInterceptedException as exc:
            ActionChains(self.driver).move_to_element(elem).click(elem).perform()
        except selenium.common.exceptions.ElementNotInteractableException as ex:
            coord = elem.location_once_scrolled_into_view
            elem.click()

        self.sleep(DEFAULT_TIME_SLEEP)
