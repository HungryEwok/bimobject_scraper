from scrapy.selector.unified import Selector
from typing import Dict


def parse_table(selector: Selector, row_xpath: str) -> Dict:
    """
    Парсинг таблицы с параметрами товара
    Возвращает словарь: ключ - название параметра,
    значение - значение параметра
    """
    parameters = {}
    for row in selector.xpath(row_xpath):
        for data in row.xpath('./*[1]//text()').getall():
            if data and not data.isspace():
                try:
                    title = ' '.join(data.split()).replace(':', '')
                except AttributeError:
                    title = data
                title = title.strip()
                break
        parameters[title] = ', '.join(
            x.strip()
            for x in row.xpath('./*[2]//text()').getall()
            if x and not x.isspace()
        )
    return parameters
