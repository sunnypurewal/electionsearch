# -*- coding: utf-8 -*-
import scrapy
import os
import json

class CbcArticlesSpider(scrapy.Spider):
  name = 'cbc-articles'
  allowed_domains = ['cbc.ca']
  publisher = "cbc"
  # headlines = []
  # index = -1
  
  def start_requests(self):
    headlines = []
    for filename in (os.listdir("archive/cbc")):
      path = f"archive/cbc/{filename}"
      if filename.find("headlines") == -1: continue
      if os.path.isdir(path): continue
      with open(f"archive/cbc/{filename}", "r") as f:
        items = json.load(f)
        headlines.extend(items)
    requests = []
    for headline in headlines:
      id = headline["id"]
      path = f"archive/{self.publisher}/articles/{id}.txt"
      if not os.path.exists(path):
        request = scrapy.Request(url=headline["url"],meta={"id":headline["id"]})
        requests.append(request)
    print (f"Fetching {len(requests)} Articles for {self.publisher}")
    return requests

  def parse(self, response):
    paragraphs = response.xpath("//div[@class='story']/span/p/text()").getall()
    id = response.meta["id"]
    with open(f"archive/cbc/articles/{id}.txt", "w") as f:
      f.write("\n".join(paragraphs))
    # self.index += 1
    # return [self.next_request()]

  # def next_request(self):
  #   self.index += 1
  #   headline = self.headlines[self.index]
  #   for filename in (os.listdir("archive/cbc/articles")):
  #     if (filename.find(str(headline["id"])) != -1):
  #       self.index += 1
  #       return self.next_request()
  #   return scrapy.Request(url=headline["url"])

