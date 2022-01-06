from typing import List

import bs4

from src.parsers.bs.maps.base_parser import BaseParser


class GoogleParser(BaseParser):

    def parsing(self):
        need_divs: List[bs4.element.Tag] = self.soup.find_all('div', {"class": 'ODSEW-ShBeI NIyLF-haAclf gm2-body-2'})
        data = []
        for div in need_divs:
            content = div.find('div', {"class": "ODSEW-ShBeI-content"})

            title: bs4.element.Tag = content.find('div', {"class": "ODSEW-ShBeI-RWgCYc ODSEW-ShBeI-RWgCYc-SfQLQb-BKD3ld"})
            grade_and_date: bs4.element.Tag = content.find('div', {"class": "ODSEW-ShBeI-jfdpUb"})
            review: bs4.element.Tag = content.find('div', {"class": "ODSEW-ShBeI-ShBeI-content"})

            name = title.find('div', class_='ODSEW-ShBeI-title').text

            grade = len(grade_and_date.find_all('img', {"class": "ODSEW-ShBeI-fI6EEc ODSEW-ShBeI-fI6EEc-active"}))
            date = grade_and_date.find('span', {"class": "ODSEW-ShBeI-RgZmSc-date"})

            review_text = None
            if review:
                review_text = review.find('span', {"class": "ODSEW-ShBeI-text"}).text

            data.append(
                {
                    "name": name,
                    "grade": grade,
                    "date": date.text,
                    "review_text": review_text if review_text else "",
                }
            )
        return data

