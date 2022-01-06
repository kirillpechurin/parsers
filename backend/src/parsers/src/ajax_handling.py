from src.parsers.src.base_driver import BaseDriver
from src.parsers.src.scroll import Scroll


class AjaxHandling(BaseDriver):

    def __init__(self, driver):
        super().__init__(driver)
        self.scroll = Scroll(driver)

    def get_accordance(self, method_search, value_search, count_elements):
        count_elements = count_elements if count_elements else 1000
        result = self.search_methods.find_list(method_search, value_search)
        check_result = []
        while len(result) != count_elements:
            result = self.search_methods.find_list(method_search, value_search)
            self.scroll.do_scroll_to_elem(result[-1])

            check_result.append(len(result))
            if check_result.count(check_result[-1]) >= 10:
                break
            elif check_result[-1] >= count_elements:
                break
        print('Number of results found: {} vs {}'.format(
            len(result), count_elements if count_elements != 1000 else 'default value: {}'.format(count_elements))
        )
        return result
