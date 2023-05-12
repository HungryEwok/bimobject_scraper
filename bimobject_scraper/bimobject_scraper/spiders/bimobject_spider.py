import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader
from bimobject_scraper.items import BimobjectScraperItem
from bimobject_scraper.helpers import parse_table


class BimObjectSpider(scrapy.Spider):

    name = 'bimobject'
    allowed_domains = ['www.bimobject.com']
    start_urls = ['https://www.bimobject.com/ru/categories']

    CATEGORIES_XPATH = '//div[@class="categories-container"]/ul/li/a/@href'
    ITEM_XPATH = '//div[@class="product-card-text-container"]/a[2]/@href'
    LAST_PAGE_XPATH = '//a[@data-test="go-to-last-link"]/text()'
    ITEM_CATEGORIES_XPATH = '//ul[@class="bim-breadcrumbs"]/li/a/text()'
    ITEM_TITLE_XPATH = '//h1/text()'
    PARAMS_TABLE_XPATH = (
        '//app-detailed-info[@data-test="classification-section"]//ul/li/div'
    )
    OMNI_CLASS_NUMBER = 'Номер OmniClass'
    OMNI_CLASS_NAME = 'Наименование OmniClass'

    def parse(self, response: Response):
        for href in response.xpath(self.CATEGORIES_XPATH).getall():
            yield response.follow(
                url=href,
                callback=self.parse_items
            )

    def parse_items(self, response: Response, pagination=True):
        for href in response.xpath(self.ITEM_XPATH).getall():
            yield response.follow(
                url=href,
                callback=self.parse_item
            )
        if pagination:
            last_page = response.xpath(self.LAST_PAGE_XPATH).get()
            if last_page:
                for i in range(2, int(last_page)+1):
                    yield response.follow(
                        url=f'{response.url}?page={i}/',
                        callback=self.parse_items,
                        cb_kwargs=dict(pagination=False)
                    )

    def parse_item(self, response: Response):
        loader = ItemLoader(
            item=BimobjectScraperItem(),
            selector=response
        )
        loader.add_value('url', response.url)
        loader.add_value(
            'categories',
            response.xpath(self.ITEM_CATEGORIES_XPATH).getall()[-2:]
        )
        loader.add_xpath(
            'title',
            self.ITEM_TITLE_XPATH
        )
        params = parse_table(response, self.PARAMS_TABLE_XPATH)
        loader.add_value(
            'omni_code',
            params.pop(self.OMNI_CLASS_NUMBER, None)
        )
        loader.add_value(
            'omni_class_name',
            params.pop(self.OMNI_CLASS_NAME, None)
        )
        yield loader.load_item()
