# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BbcNewshindiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_page_url = Field()

    title_headlines  = Field()

    content_news = Field()
