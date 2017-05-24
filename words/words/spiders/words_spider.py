from scrapy import Spider
from scrapy.selector import Selector

from words.items import WordsItem


class WordsSpider(Spider):
    name = "words"
    allowed_domains = ["20minutos.es"]
    start_urls = [
        "http://www.20minutos.es/noticia/3045391/0/luz-verde-remodelacion-bernabeu-entorno-con-dudas-juridicas-cs-psoe-con-hotel-pospuesto-otras-fases/",
    ]

    def parse(self, response):
        paragraphs = Selector(response).xpath('//div[@class="article-content"]')

	for paragraph in paragraphs:
            item = WordsItem()
            item['text'] = paragraph.xpath('p//text()').extract()
            yield item

