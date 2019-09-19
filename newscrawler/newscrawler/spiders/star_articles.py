# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime

class StarArticlesSpider(scrapy.Spider):
  name = 'star-articles'
  publisher = "star"
  allowed_domains = ['thestar.com']
  HOST = "https://www.thestar.com"
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
      print(headline["id"])
      request = scrapy.Request(url=headline["url"],meta={"headline":headline})
      requests.append(request)
    print (f"Fetching {len(requests)} Articles")
    return requests

  def parse(self, response):
    paragraphs = response.xpath("//div[@class='main-content']/p[@class='text-block-container']/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    print(id)
    tagstring = response.xpath("//meta[@name='news_keywords']/@content").get()
    headline["tags"] = tagstring.split(",")
    datestring = response.css("span.article__published-date::text").get()
    date = dateparser.parse(datestring)
    headline["timestamp"] = date.timestamp()
    idx = -1
    for i, h in enumerate(self.headlines):
      if h["id"] == headline["id"]: 
        idx = i
        break
    if idx != -1:
      self.headlines[idx] = headline
    if len(paragraphs) > 0:
      with open(f"archive/{self.publisher}/articles/{id}.txt", "w") as f:
        f.write("\n".join(paragraphs))
      with open(f"archive/{self.publisher}/headlines", "w") as f:
        json.dump(self.headlines, f)
    # self.index += 1
    # return [self.next_request()]

  # def next_request(self):
  #   self.index += 1
  #   # if self.index > 0:
  #     # return scrapy.Request(url="")
  #   try:
  #     headline = self.headlines[self.index]
  #     # for filename in (os.listdir(f"archive/{self.publisher}/articles")):
  #     #   if (filename.find(str(headline["id"])) != -1):
  #     #     self.index += 1
  #     #     return self.next_request()
  #     return scrapy.Request(url=headline['url'])
  #   except IndexError:
  #     return scrapy.Request(url="")
