# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime

class HeraldArticlesSpider(scrapy.Spider):
  name = 'herald-articles'
  publisher = "herald"
  allowed_domains = ['calgaryherald.com']
  headlines = []
  
  def start_requests(self):
    for filename in (os.listdir(f"archive/{self.publisher}")):
      if filename.find("headlines") == -1: continue
      path = f"archive/{self.publisher}/{filename}"
      print(path)
      if os.path.isdir(path): continue
      with open(path, "r") as f:
        items = json.load(f)
        self.headlines.extend(items)
    requests = []
    for headline in self.headlines:
      id = headline["id"]
      path = f"archive/{self.publisher}/articles/{id}.txt"
      if not os.path.exists(path):
        request = scrapy.Request(url=headline["url"],meta={"headline":headline})
        requests.append(request)
    print (f"Fetching {len(requests)} Articles")
    return requests

  def parse(self, response):
    paragraphs = response.xpath("//div[@itemprop='articleBody']/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    print(id)
    datestring = response.xpath("//head/meta[@property='article:published_time']/@content").get()
    headline["timestamp"] = dateparser.parse(datestring).timestamp()
    headline["author"] = response.xpath("//div[@class='author-wrap']/span[@class='name']/text()").get()
    tagstring = response.xpath("//meta[@name='news_keywords']/@content").get()
    if tagstring is not None:
      headline["tags"] = tagstring.split(",")
    idx = -1
    for i, h in enumerate(self.headlines):
      if h["id"] == headline["id"]: 
        idx = i
        break
    if idx != -1:
      self.headlines[idx] = headline
    if len(paragraphs) > 1:
      with open(f"archive/{self.publisher}/articles/{id}.txt", "w") as f:
        f.write("\n".join(paragraphs))
      with open(f"archive/{self.publisher}/headlines.jsonc", "w") as f:
        json.dump(self.headlines, f)