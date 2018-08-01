# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    # 每个项目唯一的名字，用以区分不同的scrapy
    name = 'quotes'
    # 允许爬取的域名，如果初始或者后续的请求链接不是这个域名下的，则请求链接会被过滤掉
    allowed_domains = ['quotes.toscrape.com']
    # 包含了Spider在启动时爬取的url列表，初始请求由它来定义
    start_urls = ['http://quotes.toscrape.com/']

    # Spider的一个方法，默认情况下，被调用时start_urls里面的链接构成的请求完成下载后，返回的想要就会
    # 作为唯一的参数传递给这个函数，该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item
        next = response.css('.pager .next a::attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)


