import scrapy
from spiders.items import ArticleItem


class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = [
        "https://vnexpress.net/my-thay-nga-thanh-nha-cung-cap-dau-tho-lon-nhat-cho-eu-4586807.html"]

    # def __init__(self, *args, **kwargs):
    #     self.url = kwargs.get('url')
    #     self.domain = kwargs.get('domain')
    #     self.start_urls = [self.url]
    #     self.allowed_domains = [self.domain]

    def parse(self, response):
        item = ArticleItem()
        # item['url'] = response.url.split("/")[-1]
        item['title'] = response.xpath(
            '//h1[@class="title-detail"]/text()').get()
        item['content'] = response.css('.fck_detail p::text').getall()
        yield (item)
