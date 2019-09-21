from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl("cbc-articles", domain="cbc.ca")
process.crawl("star-articles", domain="thestar.com")
process.crawl("globe-articles", domain="theglobeandmail.com")
process.crawl("post-articles", domain="nationalpost.com")
process.crawl("global-articles", domain="globalnews.ca")
process.crawl("macleans-articles", domain="macleans.ca")
process.crawl("herald-articles", domain="calgaryherald.com")
process.start()