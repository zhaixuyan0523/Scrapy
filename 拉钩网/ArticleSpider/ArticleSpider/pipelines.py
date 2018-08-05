# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import codecs
import json
import pymysql


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item


# 将item保存到json文件, 自定义json 文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 将item保存到json文件,调用scrapy提供的json exporter 导出json文件
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 添加了爬取拉勾网职位信息的scrapy，使用了crawl spider模板爬取
class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '19970523zxy', 'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,comment_nums,fav_nums,tags,content)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (
            item['title'], item['create_date'], item['url'], item['url_object_id'],
            item['front_image_url'], item['front_image_path'], item['praise_nums'],
            item['comment_nums'], item['fav_nums'], item['tags'], item['content'])
        )
        self.conn.commit()

<<<<<<< HEAD
=======
=======
# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.connect('localhost', 'root', '19970523zxy', 'article_spider', charset='utf8', use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = """
#             insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,front_image_path,praise_nums,comment_nums,fav_nums,tags,content)
#             values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """
#         self.cursor.execute(insert_sql, (
#             item['title'], item['create_date'], item['url'], item['url_object_id'],
#             item['front_image_url'], item['front_image_path'], item['praise_nums'],
#             item['comment_nums'], item['fav_nums'], item['tags'], item['content'])
#         )
#         self.conn.commit()


# class MysqlTwistedPipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         db_params = dict(
#             host=settings["MYSQL_HOST"],
#             db=settings["MYSQL_DBNAME"],
#             user=settings["MYSQL_USER"],
#             passwd=settings["MYSQL_PASSWORD"],
#             charset='utf8',
#             cursorclass=pymysql.cursors.DictCursor,
#             use_unicode=True,
#         )
#         # Twister 只是提供了一个异步的容器，并没有提供数据库连接，所以连接数据库还是要用 pymysql 进行连接
#         # adbapi 可以将 MySQL 的操作变为异步
#         # ConnectionPool 第一个参数是我们连接数据库所使用的 库名，这里是连接 MySQL 用的 pymysql
#         # 第二个参数就是 pymysql 连接操作数据库所需的参数，这里将参数组装成字典 db_params，当作关键字参数传递进去
#
#         dbpool = adbapi.ConnectionPool('pymysql', **db_params)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         # 使用 Twisted 将 MYSQL 插入变成异步
#         # 执行 runInteraction 方法的时候会返回一个 query 对象，专门用来处理异常
#         query = self.dbpool.runInteraction(self.do_insert, item)
#         query.addErrback(self.handle_error, item, spider)
#
#     def do_insert(self, cursor, item):
#         # 执行具体的插入操作
#         # 这里已经不需要手动 commit 了，Twisted 会自动 commit
#         insert_sql = '''
#                         insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,
#                         front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
#                         values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#                     '''
#         cursor.execute(insert_sql, (
#             item['title'], item['create_date'], item['url'], item['url_object_id'],
#             item['front_image_url'], item['front_image_path'],
#             item['comment_nums'], item['fav_nums'], item['praise_nums'], item['tags'], item['content']
#         ))
#
#     def handle_error(self, failure, item, spider):
#         # 异常处理方法，处理异步插入数据库时产生的异常
#         # failure 参数不需要我们自己传递，出现异常会自动将异常当作这个参数传递进来
#         print(f'出现异常：{failure}')
>>>>>>> 添加了拉勾网职位信息的爬虫，使用crawl spider爬取
>>>>>>> 添加了爬取拉勾网职位信息的scrapy，使用了crawl spider模板爬取

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # Twister 只是提供了一个异步的容器，并没有提供数据库连接，所以连接数据库还是要用 pymysql 进行连接
        # adbapi 可以将 MySQL 的操作变为异步
        # ConnectionPool 第一个参数是我们连接数据库所使用的 库名，这里是连接 MySQL 用的 pymysql
        # 第二个参数就是 pymysql 连接操作数据库所需的参数，这里将参数组装成字典 db_params，当作关键字参数传递进去

        dbpool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用 Twisted 将 MYSQL 插入变成异步
        # 执行 runInteraction 方法的时候会返回一个 query 对象，专门用来处理异常
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 添加了爬取拉勾网职位信息的scrapy，使用了crawl spider模板爬取
        # 执行具体的插入操作
        # 这里已经不需要手动 commit 了，Twisted 会自动 commit
        insert_sql = '''
                        insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,
                        front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    '''
        cursor.execute(insert_sql, (
            item['title'], item['create_date'], item['url'], item['url_object_id'],
            item['front_image_url'], item['front_image_path'],
            item['comment_nums'], item['fav_nums'], item['praise_nums'], item['tags'], item['content']
        ))
<<<<<<< HEAD
=======
=======
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
>>>>>>> 添加了拉勾网职位信息的爬虫，使用crawl spider爬取
>>>>>>> 添加了爬取拉勾网职位信息的scrapy，使用了crawl spider模板爬取

    def handle_error(self, failure, item, spider):
        # 异常处理方法，处理异步插入数据库时产生的异常
        # failure 参数不需要我们自己传递，出现异常会自动将异常当作这个参数传递进来
<<<<<<< HEAD
        print(f'出现异常：{failure}')
=======
<<<<<<< HEAD
        print(f'出现异常：{failure}')
=======
        print(f'出现异常：{failure}')
>>>>>>> 添加了拉勾网职位信息的爬虫，使用crawl spider爬取
>>>>>>> 添加了爬取拉勾网职位信息的scrapy，使用了crawl spider模板爬取
