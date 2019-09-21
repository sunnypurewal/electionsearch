# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime

class PostArticlesSpider(scrapy.Spider):
  name = 'post-articles'
  publisher = "post"
  allowed_domains = ['nationalpost.com']
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
        self.headlines.extend(items)
    requests = []
    for headline in self.headlines:
      id = headline["id"]
      path = f"archive/{self.publisher}/articles/{id}.txt"
      if not os.path.exists(path):
        request = scrapy.Request(url=headline["url"],meta={"headline":headline,"dont_cache":True})
        requests.append(request)
    print (f"Fetching {len(requests)} Articles")
    return requests


  def parse(self, response):
    paragraphs = response.xpath("//div[@class='story-content']/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    datestring = response.xpath("//head/meta[@property='article:published_time']/@content").get()
    headline["timestamp"] = dateparser.parse(datestring).timestamp()
    print(headline["timestamp"])
    tags = []
    for tag in response.xpath("//head/meta[@name='news_keywords']/@content").get().split(","):
      tags.append(tag.strip())
    headline["tags"] = tags
    idx = -1
    for i, h in enumerate(self.headlines):
      if h["id"] == headline["id"]:
        idx = i
        break
    if idx != -1:
      self.headlines[idx] = headline
    if (len(paragraphs) > 0):
      with open(f"archive/{self.publisher}/articles/{id}.txt", "w") as f:
        f.write("\n".join(paragraphs))
      with open(f"archive/{self.publisher}/headlines.jsonc", "w") as f:
        json.dump(self.headlines, f, default=lambda x: x.__dict__)