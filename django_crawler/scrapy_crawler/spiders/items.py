# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from django_app.models import Article


class ArticleItem(DjangoItem):
    django_model = Article
