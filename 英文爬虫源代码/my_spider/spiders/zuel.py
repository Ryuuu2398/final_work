import scrapy
from scrapy import item
from ..items import MySpiderItem

class ZuelSpider(scrapy.Spider):
    name = 'zuel'
    allowed_domains = ['english.zuel.edu.cn']
    start_urls = ['http://english.zuel.edu.cn/about/list.htm']


    def parse(self, response):
        item=MySpiderItem()
        item['content']='\n'.join(response.xpath('//*[@id="wp_content_w9_0"]/p//text()').extract())
        yield item
