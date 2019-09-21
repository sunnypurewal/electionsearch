# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime

class MacleansArticlesSpider(scrapy.Spider):
  name = 'macleans-articles'
  publisher = "macleans"
  allowed_domains = ['macleans.ca']
  HOST = "https://macleans.ca"
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
    paragraphs = response.css("span.entry-content>p::text").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    print(id)
    datestring = response.css("p.entry-date").xpath("@content").get()
    if datestring is not None:
      date = dateparser.parse(datestring)
      headline["timestamp"] = date.timestamp()
    headline["author"] = response.css("span.authorName>span>a::text").get()
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