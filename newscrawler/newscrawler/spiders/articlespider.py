# -*- coding: utf-8 -*-
import scrapy
import os
import logging
import json

class ArticleSpider(scrapy.Spider):

  def __init__(self, domain="", *args, **kwargs):
    self.path = kwargs["path"]
    self.archivedir = kwargs["archivedir"]
    self.dont_cache = kwargs["dont_cache"]
    logging.getLogger("scrapy").propagate = False

  def start_requests(self):
    headlines = []
    for filename in (os.listdir(f"{self.path}/{self.name.split('-')[0]}")):
      if filename.find("headlines") == -1: continue
      path = f"{self.path}/{self.name.split('-')[0]}/{filename}"
      if os.path.isdir(path): continue
      with open(path, "r") as f:
        print (f"Loading articles from {path}")
        items = json.load(f)
        headlines.extend(items)
    requests = []
    self.headlines = []
    for headline in headlines:
      id = headline["id"]
      path = f"{self.archivedir}/{self.name.split('-')[0]}/articles/{id}.txt"
      if not os.path.exists(path):
        self.headlines.append(headline)
        request = scrapy.Request(url=headline["url"],meta={"headline":headline,"dont_cache":self.dont_cache})
        requests.append(request)
    print (f"Fetching {len(requests)} Articles for {self.name.split('-')[0]}")
    return requests

  def save_article(self, id, paragraphs):
    if len(paragraphs) == 0: 
      return
    with open(f"{self.path}/{self.name.split('-')[0]}/articles/{id}.txt", "w") as f:
      f.write("\n".join(paragraphs))

  def closed(self, reason):
    if len(self.headlines) > 0:
      with open(f"{self.path}/{self.name.split('-')[0]}/headlines.jsonc", "w") as f:
        json.dump(self.headlines, f, default=lambda x: x.__dict__)
