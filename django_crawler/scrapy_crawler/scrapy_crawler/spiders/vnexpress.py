import scrapy
from django_app.models import Article


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

    async def parse(self, response):
        existing_article = Article.objects.filter(
            title="Test Title",
            content="Test Content"
        )
        if not await existing_article.aexists():
            article = await Article.objects.acreate(
                title="Test Title",
                content="Test Content"
            )
            print(f"Created new article: {article.title}")
        url = response.url.split("/")[-1]
        heading = response.xpath(
            '//h1[@class="title-detail"]/text()').get()
        content = response.css('.fck_detail p::text').getall()
        self.log(f'------------------ heading: {heading}, url: {url}, content: {content}')
        pass
