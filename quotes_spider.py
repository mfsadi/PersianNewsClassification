import scrapy
from scrapy.linkextractors import LinkExtractor

extractor = LinkExtractor(allow=r'https://www.isna.ir/news/.*')

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
    'https://www.isna.ir/archive?pi=1&pl=122&ms=0&dy=20&mn=8&yr=1399']
    def parse(self, response):
        yield {
        'text': response.css('div.item-text p::text').getall(),
        'subject': response.css('h1.first-title::text').get(),
        }
          
        for link in extractor.extract_links(response):
            yield response.follow(link, self.parse)
