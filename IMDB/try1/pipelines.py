# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import time
import datetime

from try1.items import Try1Item


class Try1Pipeline:
    def process_item(self, item, spider):
        # if isinstance(item, Try1Item):
        #     now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        #     item['timestamp_crawl'] = now
        return item
# items中加入时间戳
