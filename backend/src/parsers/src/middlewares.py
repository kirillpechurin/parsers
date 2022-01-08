import functools
import os

import selenium


def garbage_collector(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        response = (None, None)
        try:
            response = method(self, *args, **kwargs)
        except selenium.common.exceptions.WebDriverException as exc:
            print(exc.msg)
        except Exception as exc:
            print("Error on parsing")
        finally:
            self.driver.quit()
            try:
                os.remove(self.source_filename)
            except FileNotFoundError as exc:
                print("File not found")
                return None, None
        return response
    return wrapper
