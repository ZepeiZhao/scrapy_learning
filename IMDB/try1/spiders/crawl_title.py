import scrapy
from try1.items import Try1Item
from scrapy.crawler import CrawlerProcess
import time

class SpiderTry(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']
    start_urls = ["https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&ref_=adv_prv"]
    custom_settings = {'FEED_FORMAT': 'jsonlines', 'FEED_URI': 'Zepei_Zhao_hw01_scrapy_title.jl'}

    FEED_EXPORT_ENCODING = 'utf-8'
    count = 0
    page_end = 120
    id = 0


    def parse(self, response):

        nextPage = response.xpath('//div[@class="desc"]/a[@class="lister-page-next next-page"]/@href').extract()

        if self.count < self.page_end and nextPage is not None:
            self.count += 1
            next_url = "http://www.imdb.com"+nextPage[0]
            yield scrapy.Request(next_url,callback=self.parse)

        for href in response.xpath('//div[@class="lister-item-content"]/'
                                   'h3[@class="lister-item-header"]/a/@href').getall():
            yield response.follow(url=href,callback=self.parse_movie)

    def parse_movie(self,response):
        item = Try1Item()
        self.id = self.id + 1

        item['id'] = self.id
        item['url'] = response.url

        if isinstance(item, Try1Item):
            now = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
            item['timestamp_crawl'] = now

        item['title'] = [ x.replace('\xa0', '').rstrip()  for x in response.css(".title_wrapper h1::text").getall()][0]
        #item['genres'] = [x.strip() for x in response.xpath('//div[@class="see-more inline canwrap"]/h4[contains(., "Genres:")]/following-sibling::a/text()').getall()]

        genres = response.xpath('//div[@class="see-more inline canwrap"]/h4[contains(., "Genres:")]/following-sibling::a/text()').getall()
        if genres:
            item['genres'] = [x.strip() for x in genres]
        else:
            item['genres'] = []

        language = response.xpath('//div[@class="txt-block"]/h4[contains(., "Language:")]/following-sibling::a/text()').getall()
        if language:
            item['languages'] =language
        else:
            item['languages'] = []


        release_date = response.xpath('//div[@class="txt-block"]/h4[contains(., "Release Date:")]/following-sibling::text()').getall()
        if release_date:
            item['release_date'] = release_date[0].split("(")[0].strip()
        else:
            item['release_date'] = ''

        budget = response.xpath('//div[@class="txt-block"]/h4[contains(., "Budget:")]/following-sibling::text()').getall()
        if(budget):
            item['budget'] = budget[0].strip()
        else:
            item['budget'] = ''

        gross = response.xpath('//div[@class="txt-block"]/h4[contains(., "Cumulative Worldwide Gross:")]/following-sibling::text()').getall()
        if gross:
            item['gross'] = gross[0].strip()
        else:
            item['gross'] = ''

        runtime = response.xpath('//div[@class="txt-block"]/time/text()').getall()
        if runtime:
            item['runtime'] = runtime[0]
        else:
            item['runtime'] = ''


        return item



process = CrawlerProcess()
process.crawl(SpiderTry)
process.start()
