from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess

def update(publishers, path="tmp", dont_cache=True):
  process = CrawlerProcess(get_project_settings())

  for p in publishers:
    process.crawl(p, 
    name=p, 
    path=path, 
    dont_cache=dont_cache)

  process.start()