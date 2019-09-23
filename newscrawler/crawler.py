from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

def crawl(publishers, path="tmp", archivedir="archive", dont_cache=True):
  settings = get_project_settings()
  settings.set("FEED_URI", f"{path}/%(name)s/headlines.jsonc")
  settings.set("FEED_FORMAT", "json")
  process = CrawlerProcess(settings)

  for p in publishers:
    process.crawl(p,
    name=p,
    path=path,
    archivedir=archivedir,
    dont_cache=dont_cache)

  process.start()