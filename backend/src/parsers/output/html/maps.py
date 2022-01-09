from jinja2 import Template

from src.utils.work_json_file import WorkJsonFile

dictionary = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'cz',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': 'b',
    'э': 'e',
    'ю': 'u',
    'я': 'ja',
    ',': '',
    '?': '',
    ' ': '',
    '~': '',
    '!': '',
    '@': '',
    '#': '',
    '$': '',
    '%': '',
    '^': '',
    '&': '',
    '*': '',
    '(': '',
    ')': '',
    '-': '',
    '=': '',
    '+': '',
    ':': '',
    ';': '',
    '<': '',
    '>': '',
    '\'': '',
    "\"": '',
    '\\': '',
    '/': '',
    '№': '',
    '[': '',
    ']': '',
    '{': '',
    '}': '',
    'ґ': '',
    'ї': '',
    'є': '',
    'Ґ': '',
    'Ї': '',
    'Є': '',
    '—': ''
}

SOURCE_RENDERING_FILE = "src/parsers/tmp/maps/rendering/base_reviews.html"


def render_jinja_html(file_name, **context):
    jinja2_template_string = open(file_name, 'r').read()
    template = Template(jinja2_template_string)
    html_template_string = template.render(**context)
    return html_template_string


class RenderHTMLBody:

    def __init__(self, filename):
        self.filename = filename

    def get_slug_address(self, address):
        new_str = ''
        for item in address.lower():
            new_str += dictionary.get(item) if dictionary.get(item) else "_"
        return new_str

    def create(self, reviews: dict, info_data: dict):
        addresses = reviews.keys()
        addresses_with_reviews = [
            {
                "address": address,
                "address_id": self.get_slug_address(address),
                "reviews": reviews.get(address)
            }
            for address in addresses
        ]
        slug_addresses = [
            self.get_slug_address(address) for address in addresses
        ]
        all_count_reviews = sum([len(reviews.get(address)) for address in addresses if reviews.get(address)])
        body = render_jinja_html(
            SOURCE_RENDERING_FILE,
            slug_addresses=slug_addresses,
            addresses_with_reviews=addresses_with_reviews,
            all_count_reviews=all_count_reviews,
            organisation=info_data.get("organisation"),
            city=info_data.get("city"),
            map_name=info_data.get("map_name")
        )
        with open(self.filename, mode='w') as file:
            file.write(body)
        return self.filename
