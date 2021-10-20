import datetime
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter, is_item
from scrapy import signals


class SaveStatsInDatabaseMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_closed(self, spider, reason):
        stats = spider.crawler.stats.get_stats()
        job = {}
        job['start_timestamp'] = stats.get(
            'start_time').strftime('%Y-%m-%d %H:%M:%S')
        job['end_timestamp'] = stats.get(
            'finish_time').strftime('%Y-%m-%d %H:%M:%S')
        job['spider_name'] = spider.name
        job['items_scraped'] = stats.get('item_scraped_count')
        job['items_dropped'] = stats.get('item_dropped_count')
        job['finish_reason'] = stats.get('finish_reason')
        job['failed_urls'] = stats.get('failed_urls')
        job['failed_urls_status'] = stats.get('failed_urls_status')
        job['stats'] = repr(stats)
        job['postal_code'] = spider.postal_code
        with open('stats.json', 'w', newline='') as outputdata:
            json.dump(job, outputdata)
