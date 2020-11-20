import scrapy
from urllib.parse import unquote


class RooketSpider(scrapy.Spider):
    name = "rooket"
    api_url = "https://roocket.ir/search?search="
    custome_urls = []
    counter = 0

    f = open('rooket_log.txt', 'w', encoding='utf-8')
    f.close()
    tags = open('tags.txt', 'r', encoding='utf-8').readlines()
    for tag in tags:
        custome_urls.append(api_url + tag.strip())

    def start_requests(self):
        for url in RooketSpider.custome_urls:
            self.counter += 1
            f = open('rooket_log.txt', 'a', encoding='utf-8')
            f.write("now processing " + str(url) + "\n")
            f.close()
            print("Processing ... " + str(round(((self.counter / len(RooketSpider.custome_urls)) * 100), 2)) + " %")
            yield scrapy.Request(url)

    def parse(self, response):

        if response.css('div.content p::text').get():
            p = response.css('div.content div.subject_tags a::text').getall()
            p.append(response.meta['s_tag'])
            yield {
                'text': response.css('div.content p::text').getall(),
                'subject': response.css('h1.title::text').get(),
                'tag': p,
            }
        next_page_url = response.css('div.search-results__section h3 a::attr(href)').getall()
        for page in next_page_url:
            yield scrapy.Request(response.urljoin(page), meta={'s_tag': unquote(response.request.url.split("=")[1])})
        for number in range(2, 20):  # make 100 later
            yield scrapy.Request(response.urljoin(response.request.url + "&page=" + str(number) + "#search-page"),
                                 meta={'s_tag': unquote(response.request.url.split("=")[1])})
