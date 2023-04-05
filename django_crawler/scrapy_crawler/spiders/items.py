# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy_djangoitem import DjangoItem
from django_app.models import Article
from django_app.models import Category


class CategoryItem(DjangoItem):
    django_model = Category


class ArticleItem(DjangoItem):
    django_model = Article
    categories = scrapy.Field()
