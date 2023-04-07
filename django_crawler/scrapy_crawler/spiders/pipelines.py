# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from django_app.models import Article, Category
from spiders.items import ArticleItem, CategoryItem


class ScrapyVnexpressPipeline:
    def process_item(self, item, spider):
        if (isinstance(item, ArticleItem)):
            categories = item['categories']
            model = item.save()
            for category in categories:
                model.categories.add(category)
        elif (isinstance(item, CategoryItem)):
            if Category.objects.filter(slug=item['slug']).exists():
                return
            item.save()
        return item
