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
        item['title'] = response.xpath(
            '//h1[@class="title-detail"]/text()').get()
        item['content'] = "".join(response.css(
            '.fck_detail > p::text').getall())
        item['url'] = response.url
        item['author'] = "".join(response.css(
            '.fck_detail > p')[-1].css('p ::text').getall())
        yield (item)
