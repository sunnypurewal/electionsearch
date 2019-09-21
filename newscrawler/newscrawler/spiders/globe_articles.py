# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime

class GlobeArticlesSpider(scrapy.Spider):
  name = 'globe-articles'
  publisher = "globe"
  allowed_domains = ['theglobeandmail.com']
  headlines = []
  
  def start_requests(self):
    paths = []
    for filename in (os.listdir(f"archive/{self.publisher}")):
      if filename.find("headlines") == -1: continue
      path = f"archive/{self.publisher}/{filename}"
      if os.path.isdir(path): continue
      paths.append(path)
    paths.sort()
    for path in paths:
      with open(path, "r") as f:
        items = json.load(f)
        self.headlines.append(items)
    requests = []
    for row in self.headlines:
      for headline in row:
        id = headline["id"]
        path = f"archive/{self.publisher}/articles/{id}.txt"
        if not os.path.exists(path):
          request = scrapy.Request(url=headline["url"],meta={"headline":headline})
          requests.append(request)
    print (f"Fetching {len(requests)} Articles")
    return requests

  def parse(self, response):
    paragraphs = response.css("p.c-article-body__text::text").getall()
    headline = response.meta["headline"]
    author = response.css(".c-byline::text").get()
    if author is not None:
      author = author.strip()
      headline["author"] = author
    id = headline["id"]
    tagstring = response.xpath("//head/meta[@name='news_keywords']/@content").get()
    if tagstring is not None:
      tags = []
      for tag in tagstring.split(","):
        tags.append(tag.strip())
      headline["tags"] = tags
    time = int(response.css("time").xpath("@data-unixtime").get())
    headline["timestamp"] = time
    idx = -1
    for i, h in enumerate(self.headlines):
        if h["id"] == headline["id"]:
          idx = i
          break
    if idx != -1:
      self.headlines[idx] = headline
    if (len(paragraphs) > 0):
      path = f"archive/{self.publisher}/articles/{id}.txt"
      if not os.path.exists(path):
        with open(f"archive/{self.publisher}/articles/{id}.txt", "w") as f:
          f.write("\n".join(paragraphs))
      with open(f"archive/{self.publisher}/headlines.jsonc", "w") as f:
        json.dump(self.headlines[idx], f, default=lambda x: x.__dict__)