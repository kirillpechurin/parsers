from typing import List

import bs4

from src.parsers.bs.maps.base_parser import BaseParser


class YandexParser(BaseParser):

    def parsing(self):
        need_divs: List[bs4.element.Tag] = self.soup.find_all('div', {"class": 'business-review-view__info'})
        data = []
        for div in need_divs:
            div_children: list = list(div.children)
            href_icon: bs4.element.Tag = div_children[0]
            title: bs4.element.Tag = div_children[1]
            grade_and_date: bs4.element.Tag = div_children[2]
            text_review: bs4.element.Tag = div_children[3]

            name = title.find('span').text
            grade = len(grade_and_date.find_all('span', class_='inline-image _loaded business-rating-badge-view__star _size_m'))
            date = grade_and_date.find('span', class_='business-review-view__date').text
            text_review = text_review.find('span', class_='business-review-view__body-text').text

            data.append(
                {
                    "name": name,
                    "grade": grade,
                    "date": date,
                    "text_review": text_review,
                }
            )
        return data
