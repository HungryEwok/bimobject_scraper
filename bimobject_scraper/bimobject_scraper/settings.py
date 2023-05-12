import os
from dotenv import load_dotenv


load_dotenv()

BOT_NAME = 'bimobject_scraper'

SPIDER_MODULES = ['bimobject_scraper.spiders']
NEWSPIDER_MODULE = 'bimobject_scraper.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0.5

CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Раскомментировать для записи в ElasticSearch
ITEM_PIPELINES = {
    'bimobject_scraper.pipelines.BimobjectScraperJsonPipeline': 500,
    # 'bimobject_scraper.pipelines.BimobjectScraperElasticSearchPipeline': 500,
}


AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 32

SPIDERMON_ENABLED = True
EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
FEED_EXPORT_ENCODING = 'utf-8'

ELASTICSEARCH_SERVERS = os.getenv('ES_HOST')
ELASTICSEARCH_INDEX = os.getenv('ES_INDEX')
ELASTICSEARCH_TYPE = 'items'
