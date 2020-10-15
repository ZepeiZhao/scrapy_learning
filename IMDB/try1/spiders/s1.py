import scrapy
from try1.items import Try1Item
from scrapy.crawler import CrawlerProcess
import time

class SpiderTry(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['imdb.com']

    #start_urls = ["https://www.imdb.com/search/title/?genres=comedy&start=%d&explore=title_type,genres&ref_=adv_nxt"% n for n in range(1,201,50)]

    start_urls = ["https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&ref_=adv_prv"]
    custom_settings = {'FEED_FORMAT': 'json', 'FEED_URI': 'IMDBtry1.jl'}

    FEED_EXPORT_ENCODING = 'utf-8'
    count = 1
    page_end = 10


    # def start(self):
    #     url = response.xpath('//a[@class="lister-page-next next-page"]/@href').extract()[0]
    #
    #     yield scrapy.request("http://imdb.com/"+url,callback=self.parse)

    id = 0
    def parse(self, response):

        # url = response.xpath('//a[@class="lister-page-next next-page"]/@href').extract()[0]
        #
        # yield scrapy.Request("http://www.imdb.com/" + url, callback=self.parse)
        #
        nextPage = response.xpath('//div[@class="desc"]/a[@class="lister-page-next next-page"]/@href').extract()

        if self.count < self.page_end and nextPage is not None:
            self.count += 1
            next_url = "http://www.imdb.com" + nextPage[0]
            yield scrapy.Request(next_url, callback=self.parse)

        for href in response.xpath('//div[@class="lister-item-content"]/'
                                   'h3[@class="lister-item-header"]/a/@href').getall():

            yield response.follow(url=href,callback=self.parse_movie)

    def parse_movie(self,response):
        self.id  = self.id +  1
        item = Try1Item()
        item['id'] = self.id
        item['url'] = response.url

        if isinstance(item, Try1Item):
            now = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
            item['timestamp_crawl'] = now

        item['title'] = [ x.replace('\xa0', '').rstrip()  for x in response.css(".title_wrapper h1::text").getall()][0]
        item['genres'] = [x.strip() for x in response.xpath('//div[@class="see-more inline canwrap"]/h4[contains(., "Genres:")]/following-sibling::a/text()').getall()]
        item['languages'] = response.xpath('//div[@class="txt-block"]/h4[contains(., "Language:")]/following-sibling::a/text()').getall()
        item['release_date'] = response.xpath('//div[@class="txt-block"]/h4[contains(., "Release Date:")]/following-sibling::text()').getall()[0].replace('(USA)','').strip()

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



        # nextPage = response.xpath('//div[@class="desc"]/a[@class="lister-page-next next-page"]/@href').extract()
        #
        # if self.count < self.page_end and nextPage is not None:
        #     self.count += 1
        #     next_url = "http://www.imdb.com"+nextPage[0]
        #     yield scrapy.Request(next_url,callback=self.parse)

process = CrawlerProcess()
process.crawl(SpiderTry)
process.start()
