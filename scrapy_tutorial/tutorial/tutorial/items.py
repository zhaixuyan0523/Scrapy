# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# 是保存爬取数据的容器，它的使用方法和字典类似，但多了额外的保护机制，可以避免拼写错误或者定义字段错误
# 创建Item需要继承scrapy.Item类，并且定义类型为scrapy.field的字段
import scrapy


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
