import scrapy
#from scrapy.linkextractors import LinkExtractor

#extractor = LinkExtractor(allow=r'https://www.isna.ir/news/.*')

class VirgoolSpider(scrapy.Spider):
    name = "virgool"
    api_url="https://virgool.io/tag/%DA%AF%D9%88%DA%AF%D9%84-%DA%A9%D8%B1%D9%88%D9%85?page="
    start_urls = [api_url + '1']
    def parse(self, response):
        yield {
        'text': response.css('div.post-body p::text').getall(),
        'subject': response.css('div.post-content h1::text').get(),
        }
          
        #for link in extractor.extract_links(response):
        #    yield response.follow(link, self.parse)
        next_page_url = response.css("div.post-content > a::attr(href)").getall()
        print ("THESE ARE URLS: ")
        print(next_page_url)
        for page in next_page_url:
            yield scrapy.Request(response.urljoin(page))
        for number in range (2, 20):
            yield scrapy.Request(response.urljoin(VirgoolSpider.api_url+str(number)))


'''
class MySpider(BaseSpider):
    name = 'website.com'
    baseUrl = "http://website.com/page/"

    def start_requests(self):
        yield Request(self.baseUrl + '0')

    def parse(self, response):
        if response.status != 404:
            page = response.meta.get('page', 0) + 1
            return Request('%s%s' % (self.baseUrl, page), meta=dict(page=page))
			'''