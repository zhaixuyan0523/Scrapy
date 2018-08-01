# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# Item Pipeline 为项目管道，当Item生成后，它会自动被送到Item Pipeline进行处理，常使用Item Pipeline进行如下操作：
# 1、清理HTML数据
# 2、验证爬取的数据，检查爬取字段
# 3、查重杯丢弃重复内容
# 4、将爬取结果保存到数据库
# 要实现Item Pipeline，只需要定义一个类并实现process_item()方法即可。启用Item Pipeline后，Item Pipeline会自动调用这个方法。
# process_item()方法必须返回包含数据的字典或者Item对象或者抛出DropItem()异常
# process_item()方法有两个参数，一个是item ，每次Spider生成的Item都会作为参数传递过来，另一个是spider，就是Spider的实例

from scrapy.exceptions import DropItem
import pymongo


class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 是一种依赖注入的方式，参数为crawler，通过crawler可以拿到全局配置的每个配置信息，在全局设置中，可以定义MONGO_URI和MONGO_DB
    # 来指定MongoDB连接需要的地址和数据库名称，拿到配置信息之后返回类对象即可
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    # 当Spider开启时，此方法被调用，上文程序中主要进行了一些初始化操作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    # 当Spider关闭时，此方法会调用，上文程序中将数据库连接关闭
    def close_spider(self):
        self.client.close()