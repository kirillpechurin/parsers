from src.parsers.src.const import DEFAULT_TIME_SLEEP
from src.parsers.src.my_driver import Driver


class Scroll(Driver):

    def __init__(self, driver):
        super().__init__(driver=driver)

    def do_scroll_to_elem(self, elem):
        self.driver.execute_script("arguments[0].scrollIntoView();", elem)
        self.sleep(DEFAULT_TIME_SLEEP)
