# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime

class GlobalArticlesSpider(scrapy.Spider):
  name = 'global-articles'
  publisher = "global"
  allowed_domains = ['globalnews.ca']
  HOST = "https://globalnews.ca"
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
    paragraphs = response.css("span.gnca-article-story-txt").xpath("p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    print(id)
    tagstring = response.xpath("//body/meta[@name='news_keywords']/@content").get()
    headline["tags"] = tagstring.split(",")
    datestring = response.xpath("//head/meta[@name='pubdate']/@content").get()
    date = dateparser.parse(datestring)
    headline["timestamp"] = date.timestamp()
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