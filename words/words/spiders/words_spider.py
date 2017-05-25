from scrapy import Spider
from scrapy.selector import Selector
from scrapy import Request

from words.items import WordsItem


class WordsSpider(Spider):
    name = "words"
    allowed_domains = ["20minutos.es"]
    start_urls = [
        "http://www.20minutos.es/archivo/2017/02/14/",
    ]
    # Cogemos todo lo que haya despues de "archivo/"
    publication_date = "2017/02/14"

    def parse(self, response):
        news = Selector(response).xpath('//ul[@class="sub-list"]/li')

	# Visit each new an
	for new in news:
	    item = WordsItem()
	    url_to_new = new.xpath('a/@href').extract()[0]
	    yield Request(url_to_new, callback=self.parse_attr)

    def parse_attr(self, response):
	    paragraphs = Selector(response).xpath('//div[@class="article-content"]')
            for paragraph in paragraphs:
		    item = WordsItem()
		    item['text'] = paragraph.xpath('p//text()').extract()
		    item['publication_date'] = self.publication_date
		    yield item

