from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess

def update(publishers, archivedir, path="tmp", dont_cache=True):
  process = CrawlerProcess(get_project_settings())

  for p in publishers:
    process.crawl(f"{p}-articles", 
    name=f"{p}-articles", 
    archivedir=archivedir, 
    path=path, 
    dont_cache=dont_cache)

  process.start()