from selenium.webdriver.common.by import By


class BaseSearchMethods:

    @staticmethod
    def find(obj, method, value):
        raise NotImplemented


class ListSearchMethods(BaseSearchMethods):

    @staticmethod
    def find(obj, method, value):
        return obj.find_elements(method, value)


class OneSearchMethods(BaseSearchMethods):

    @staticmethod
    def find(obj, method, value):
        return obj.find_element(method, value)


class SearchMethods:

    def __init__(self, driver):
        self.list_methods = {
            "class_name": By.CLASS_NAME,
            "xpath": By.XPATH,
            'link_text': By.LINK_TEXT
        }
        self.driver = driver

    def find_list(self, method, value):
        return ListSearchMethods.find(self.driver, self.list_methods[method], value)

    def find_one(self, method, value):
        return OneSearchMethods.find(self.driver, self.list_methods[method], value)

    def find_one_at_object(self, obj, method, value):
        return OneSearchMethods.find(obj, self.list_methods[method], value)

    def find_list_at_object(self, obj, method, value):
        return ListSearchMethods.find(obj, self.list_methods[method], value)
