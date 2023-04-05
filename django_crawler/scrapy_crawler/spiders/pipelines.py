# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from spiders.items import ArticleItem, CategoryItem


class ScrapyVnexpressPipeline:
    def process_item(self, item, spider):
        if (isinstance(item, ArticleItem)):
            categories = item['categories']
            model = item.save()
            for category in categories:
                model.categories.add(category)
        else:
            item.save()  # save it to database
            return item
