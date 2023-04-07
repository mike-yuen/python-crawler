from typing import List
from django_app.models import Article, Category
from spiders.items import ArticleItem, CategoryItem
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import scrapy
import logging
import time

from selenium.webdriver.remote.remote_connection import LOGGER
# Prevent the extremely long logs from Selenium remote_connection logger
LOGGER.setLevel(logging.WARNING)

MAIN_URL = "https://vnexpress.net"


class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = [MAIN_URL]

    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome()

    def format_raw_date(self, date_string: str):
        datetime_object = datetime.strptime(
            date_string, "%d/%m/%Y, %H:%M (%z)")
        return datetime_object

    def is_ads(self, url):
        return url.find(MAIN_URL) != 0

    def parse(self, response):
        self.driver.get(response.url)
        # Must use Selenium here, ul.sub only appears after the browser's popped up
        menu_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                  ".main-nav > ul > li.kinhdoanh ul.sub > li")

        parent_category_item = CategoryItem()
        parent_category_item['title'] = "Kinh doanh"
        parent_category_item['slug'] = "kinh-doanh"
        yield (parent_category_item)

        url_list: List[str] = []
        parent_category = Category.objects.filter(
            slug="kinh-doanh").first()

        for element in menu_elements:
            url = element.find_element(
                By.TAG_NAME, "a").get_attribute("href")

            category_item = CategoryItem()
            category_item['title'] = element.find_element(
                By.TAG_NAME, "a").get_attribute("title")
            category_item['slug'] = url.split("/")[-1]
            category_item['parent'] = parent_category
            yield (category_item)
            url_list.append(url)

        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        self.driver.get(response.url)
        article_elements = self.driver.find_elements(By.CSS_SELECTOR,
                                                     "article.item-news")
        article_url_list: List[str] = []
        for element in article_elements:
            url_element = element.find_element(
                By.CSS_SELECTOR, ".thumb-art > a")
            if url_element:
                article_url_list.append(url_element.get_attribute("href"))

        categories_str = response.url.split('/')[-2:]
        categories = response.meta.get("categories") if response.meta.get(
            "categories") else Category.objects.filter(slug__in=categories_str)

        for url in article_url_list:
            if not self.is_ads(url):
                time.sleep(0.3)
                yield response.follow(url, callback=self.parse_article, meta={'categories': categories})

        # Follow next page
        next_page = response.css(
            '#pagination a.next-page::attr(href)').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = MAIN_URL + next_href
            yield response.follow(url=next_page_url, callback=self.parse_page, meta={'categories': categories})

    def parse_article(self, response):
        item = ArticleItem()
        item['url'] = response.url

        # Check if a record with a specific field value already exists
        if Article.objects.filter(url=item['url']).exists():
            return

        raw_title_element = response.xpath(
            '//h1[@class="title-detail"]/text()') or response.xpath(
            '//h1[@class="title-post"]/text()')
        item['title'] = raw_title_element.get()

        item['content'] = "".join(response.css(
            '.fck_detail p:not([style*="text-align:right;"])')[:-1].css('p ::text').getall())

        raw_authur = response.css('.fck_detail p.author_mail') or response.css('.fck_detail p.Normal[align="right"]') or response.css(
            '.fck_detail p.Normal[style*="text-align:right;"]') or response.css('.fck_detail p[style*="text-align:right;"]')
        if raw_authur:
            item['author'] = "".join(raw_authur[-1].css('p ::text').getall())

        raw_date_element = response.css('.header-content .date::text')
        if raw_date_element:
            raw_date = raw_date_element.get().split(', ')[1:]
            raw_date[1] = raw_date[1].replace("GMT+7", "+0700")
            raw_date = ', '.join(raw_date)
            datetime_object = self.format_raw_date(raw_date)
            item['published_date'] = datetime_object

        item['categories'] = response.meta.get("categories")
        yield (item)
