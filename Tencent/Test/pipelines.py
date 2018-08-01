# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.exporters import JsonItemExporter


class TestPipeline(object):

    def process_item(self, item, spider):
        return item


# 自定义 Pipeline 存储 Json 数据
class Tencent2pipeline(object):
    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('result.json', 'w', encoding='utf-8')

    # 存储数据，将 Item 实例作为 json 数据写入到文件中
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item
    # 处理结束后关闭 文件 IO 流

    def close_spider(self, spider):
        self.file.close()
# 使用 Scrapy 提供的 exporter 存储 Json 数据
# class sonExporterPipeline:
#     # 调用 scrapy 提供的 json exporter 导出 json 文件
#     def __init__(self):
#         self.file = open('questions_exporter.json', 'wb')
#         # 初始化 exporter 实例，执行输出的文件和编码
#         self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
#         # 开启倒数
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     # 将 Item 实例导出到 json 文件
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item


