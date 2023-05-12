from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapyelasticsearch.scrapyelasticsearch import ElasticSearchPipeline
import logging
import json


def filter_empty_item(item):
    adapter = ItemAdapter(item)
    if not all(
        [
            adapter.get('title'),
            adapter.get('omni_code'),
            adapter.get('omni_class_name')
        ]
    ):
        raise DropItem(
            f'Отсутствует обязательное значение у позиции {item["url"]}'
        )
    adapter['title_rus'] = ''
    adapter['omni_class_name_rus'] = ''
    return item


class BimobjectScraperElasticSearchPipeline(ElasticSearchPipeline):
    """
    Пайплайн записи собранных данных в ElasticSearch
    """
    def process_item(self, item, spider):
        item = filter_empty_item(item)
        return super().process_item(item, spider)

    def send_items(self):
        logging.debug('Данные отправлены в ElasticSearch')
        return super().send_items()


class BimobjectScraperJsonPipeline:
    """
    Пайплайн записи собранных данных в локальный JSON файл
    """
    def open_spider(self, spider):
        self.file = open('items.jsonl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        item = filter_empty_item(item)
        data = json.dumps(
            ItemAdapter(item).asdict(), ensure_ascii=False
        ) + '\n'
        self.file.write(data)
        return item
