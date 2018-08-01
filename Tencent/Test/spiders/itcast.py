# -*- coding: utf-8 -*-
import scrapy
from Test.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['www.itcast.cn']
    start_urls = ("http://www.itcast.cn/channel/teacher.shtml",)

    def parse(self, response):

        node_list = response.css(".li_txt")
        items = []
        for node in node_list:
            item = ItcastItem()
            name = node.css("h3::text").extract()
            level = node.css("h4::text").extract()
            info = node.css("p::text").extract()

            item["name"] = name[0]
            item["level"] = level[0]
            item["info"] = info[0]
            items.append(item)
        return items






