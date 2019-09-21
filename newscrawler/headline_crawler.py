from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

if not os.path.exists("archive"):
  os.mkdir("archive")

publishers = ["cbc", "star", "globe", "post", "global", "macleans", "herald"]

for p in publishers:
  if not os.path.exists(f"archive/{p}"):
    os.mkdir(f"archive/{p}")
    os.mkdir(f"archive/{p}/articles")

process = CrawlerProcess(get_project_settings())

process.crawl("cbc", domain="cbc.ca")
process.crawl("star", domain="thestar.com")
process.crawl("globe", domain="theglobeandmail.com")
process.crawl("post", domain="nationalpost.com")
process.crawl("global", domain="globalnews.ca")
process.crawl("macleans", domain="macleans.ca")
process.crawl("herald", domain="calgaryherald.com")
process.start()