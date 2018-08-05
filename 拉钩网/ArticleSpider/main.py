import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
<<<<<<< HEAD
execute(["scrapy", "crawl", "jobbole"])
=======
<<<<<<< HEAD
execute(["scrapy", "crawl", "jobbole"])
=======
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "lagou"])
>>>>>>> 添加了拉勾网职位信息的爬虫，使用crawl spider爬取
>>>>>>> 添加了爬取拉勾网职位信息的scrapy，使用了crawl spider模板爬取
