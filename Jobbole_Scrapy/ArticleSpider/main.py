from scrapy.cmdline import execute
import sys
import os

# 将当前项目目录追加到 Python 搜索模块路径
# os.path.abspath(__file__) 是当前文件
# os.path.dirname(os.path.abspath(__file__)) 是获取当前文件所在目录名
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 执行命令启动爬虫
execute(["scrapy", "crawl", "jobbole"])