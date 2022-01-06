import time


class TimeDriverMixin:

    @staticmethod
    def sleep(time_sleep):
        time.sleep(time_sleep)

    @staticmethod
    def set_implicitly_wait(wd, value):
        wd.implicitly_wait(value)
