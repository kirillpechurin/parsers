import os

from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options

from src.parsers.web import map_review_classes


def get_map_by_name(map_name):
    return map_review_classes.get(map_name)


def get_driver():
    display = Display(visible=False, size=(800, 600))
    options = Options()
    options.add_argument("--headless")
    display.start()
    return webdriver.Firefox(options=options), display


def move_file(old_path, new_path, replace_on_empty=None):
    os.replace(old_path, new_path)
    if replace_on_empty:
        new_path.replace(replace_on_empty, "")
    return new_path
