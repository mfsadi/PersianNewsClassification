import scrapy


class VirgoolSpider(scrapy.Spider):
    name = "virgool"
    api_url = "https://virgool.io/tag/"
    custome_urls = []
    counter = 0
    f = open('virgool_log.txt', 'w', encoding='utf-8')
    f.close()
    tags = open('output/tags_rem.txt', 'r', encoding='utf-8').readlines()
    for tag in tags:
        custome_urls.append(api_url + tag.strip() + '?page=1')

    def start_requests(self):
        for url in VirgoolSpider.custome_urls:
            self.counter += 1
            f = open('virgool_log.txt', 'a', encoding='utf-8')
            f.write("now processing " + str(url) + "\n")
            f.close()
            print("Processing ... " + str(round(((self.counter / len(VirgoolSpider.custome_urls)) * 100), 2)) + " %")
            yield scrapy.Request(url)

    def parse(self, response):

        if response.css('div.post-content h1::text').get():
            yield {
                'text': response.css('div.post-body p::text').getall(),
                'subject': response.css('div.post-content h1::text').get(),
                'tag': response.css('div.post-tags a::text').getall(),
            }
            pass
        next_page_url = response.css("div.post-content > a::attr(href)").getall()
        for page in next_page_url:
            yield scrapy.Request(response.urljoin(page))
        for number in range(2, 100):  # make 20 later
            yield scrapy.Request(response.urljoin(response.request.url[:-1] + str(number)))
