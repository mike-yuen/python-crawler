from typing import List
from django_app.models import Category
from spiders.items import ArticleItem, CategoryItem
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import scrapy
import logging

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
        return url.index(MAIN_URL) != 0

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
            article_url_list.append(element.find_element(
                By.CSS_SELECTOR, ".thumb-art > a").get_attribute("href"))

        categories_str = response.url.split('/')[-2:]
        categories = Category.objects.filter(slug__in=categories_str)
        for url in article_url_list:
            if not self.is_ads(url):
                yield response.follow(url, callback=self.parse_article, meta={'categories': categories})

    def parse_article(self, response):
        item = ArticleItem()
        item['title'] = response.xpath(
            '//h1[@class="title-detail"]/text()').get()
        item['content'] = "".join(response.css(
            '.fck_detail > p')[:-1].css('p ::text').getall())
        item['url'] = response.url
        item['author'] = "".join(response.css(
            '.fck_detail > p')[-1].css('p ::text').getall())

        raw_date = response.css(
            '.header-content .date::text').get().split(', ')[1:]
        raw_date[1] = raw_date[1].replace("GMT+7", "+0700")
        raw_date = ', '.join(raw_date)
        datetime_object = self.format_raw_date(raw_date)
        item['published_date'] = datetime_object
        item['categories'] = response.meta.get("categories")
        yield (item)
