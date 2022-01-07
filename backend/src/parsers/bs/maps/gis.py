from typing import List

import bs4

from src.parsers.bs.maps.base_parser import BaseParser


class GisParser(BaseParser):

    def parsing(self):
        need_divs: List[bs4.element.Tag] = self.soup.find_all('div', {"class": '_11gvyqv'})
        data = {}
        for div in need_divs:
            div_children: list = list(div.children)

            title: bs4.element.Tag = div_children[0]
            address: bs4.element.Tag = div_children[1]
            empty_div: bs4.element.Tag = div_children[2]
            review: bs4.element.Tag = div_children[3]

            name = title.find('span', class_='_16s5yj36').text
            date_review = title.find('div', class_='_4mwq3d').text
            grade_common = title.find('div', class_='_1fkin5c')

            address = address.text

            text_review = review.find('div', class_='_49x36f').text

            if not data.get(address):
                data[address] = []

            data[address].append(
                {
                    "name": name,
                    "date": date_review,
                    "grade": len(grade_common.find_all('span')),
                    "text_review": text_review,
                }
            )
        return data
