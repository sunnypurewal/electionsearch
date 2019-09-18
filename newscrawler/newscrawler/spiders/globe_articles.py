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
    paragraphs = response.css("p.c-article-body__text::text").getall()
    author = response.css(".c-byline::text").get()
    if author is not None:
      author = author.strip()
      self.headlines[self.row][self.col]["author"] = author
    id = self.headlines[self.row][self.col]["id"]
    tagstring = response.xpath("//head/meta[@name='news_keywords']/@content").get()
    if tagstring is not None:
      tags = []
      for tag in tagstring.split(","):
        tags.append(tag.strip())
      self.headlines[self.row][self.col]["tags"] = tags
    if (len(paragraphs) > 0):
      path = f"archive/{self.publisher}/articles/{id}.txt"
      if not os.path.exists(path):
        with open(f"archive/{self.publisher}/articles/{id}.txt", "w") as f:
          f.write("\n".join(paragraphs))
      with open(f"archive/{self.publisher}/headlines-{self.row+1}", "w") as f:
        json.dump(self.headlines[self.row], f, default=lambda x: x.__dict__)
    return [self.next_request()]

  def next_request(self):
    if not self.next_index(): return None
    headline = self.headlines[self.row][self.col]
    # for filename in (os.listdir(f"archive/{self.publisher}/articles")):
    #   if (filename.find(str(headline["id"])) != -1):
    #     return self.next_request()
    return scrapy.Request(url=headline['url'])

  def next_index(self):
    print(self.row, self.col, len(self.headlines[self.row]))
    if self.row == 0 and self.col == 0:
      self.row = 0
      self.col = 2
      return True
    elif self.row == 0 and self.col == 5:
      self.col = 7
      return True
    elif self.row == 1 and self.col == 1:
      self.col = 3
      return True
    elif self.row == 3 and self.col == 2:
      self.col = 4
      return True
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
    
    