import scrapy

class ArxivSpider(scrapy.Spider):
    name = 'arxiv'
    start_urls = ['https://arxiv.org/list/hep-th/recent']

    def parse(self, response):
        for title in response.css('.list-title'):
            yield {'title': title.css('::text').get().strip()}
