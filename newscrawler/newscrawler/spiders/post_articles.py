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
  row = -1
  col = -1
  
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
    return [self.next_request()]

  def parse(self, response):
    paragraphs = response.xpath("//div[@class='story-content']/p/text()").getall()
    id = self.headlines[self.row][self.col]["id"]
    datestring = " ".join(response.css("time.pubdate::text").getall())
    date = dateparser.parse(datestring)
    tags = []
    for tag in response.xpath("//head/meta[@name='news_keywords']/@content").get().split(","):
      tags.append(tag.strip())
    self.headlines[self.row][self.col]["timestamp"] = date.timestamp()
    self.headlines[self.row][self.col]["tags"] = tags
    if (len(paragraphs) > 0):
      with open(f"archive/{self.publisher}/articles/{id}.txt", "w") as f:
        f.write("\n".join(paragraphs))
      with open(f"archive/{self.publisher}/headlines-{self.row+1}", "w") as f:
        json.dump(self.headlines[self.row], f, default=lambda x: x.__dict__)
    return [self.next_request()]

  def next_request(self):
    if not self.next_index(): return None
    headline = self.headlines[self.row][self.col]
    for filename in (os.listdir(f"archive/{self.publisher}/articles")):
      if (filename.find(str(headline["id"])) != -1):
        return self.next_request()
    return scrapy.Request(url=headline['url'])

  def next_index(self):
    print(self.row, self.col, len(self.headlines[self.row]))
    if self.row == -1:
      self.row = 0
      self.col = 0
      return True
    elif self.col+1 == len(self.headlines[self.row]) and self.row+1 < len(self.headlines):
      self.row += 1
      self.col = 0
      return True
    elif self.col+1 < len(self.headlines[self.row]):
      self.col += 1
      return True
    return False
    
    