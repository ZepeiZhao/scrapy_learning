# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Try1Item(scrapy.Item):

    id = scrapy.Field()
    url = scrapy.Field()  # url
    timestamp_crawl = scrapy.Field()
    title = scrapy.Field()  # movie name
    genres = scrapy.Field()
    languages = scrapy.Field()
    release_date = scrapy.Field()
    budget = scrapy.Field()
    gross = scrapy.Field()
    runtime = scrapy.Field()

