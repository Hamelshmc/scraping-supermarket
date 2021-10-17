# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SupermarketsPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class CookiesPipeline(object):

    def process_request(self, request, spider):
        with open('./spiders/cookietest.json', 'r', newline='') as inputdata:
            cookies = json.load(inputdata)
            print(cookies)
            for cookie in cookies:
                request.cookies[cookie['name']] = cookie['value']
        return request
