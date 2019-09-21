# -*- coding: utf-8 -*-
import scrapy
import random
import json


class StarSpider(scrapy.Spider):
  name = 'star'
  allowed_domains = ['thestar.com']
  HOST = 'https://www.thestar.com/news/federal-election.html'
  domain = 'https://www.thestar.com'

  def start_requests(self):
    return [scrapy.Request(url=self.HOST,meta={"dont_cache":True})]

  def parse(self, response):
    stories = response.css(".story")
    headlines = []
    for story in stories:
      headline = {}
      a = story.xpath("div[@class='story__body']/span/span/a")
      url = f"https://www.thestar.com{a.xpath('@href').get()}"
      title = a.xpath("span[@class='story__headline']/text()").get()
      title2 = a.xpath("p[@class='story__abstract']/text()").get()
      headline["url"] = url
      headline["title"] = title
      headline["title2"] = title2
      headline["id"] = url.split("/")[-1].split(".")[0]
      headlines.append(headline)
    if len(headlines) > 0:
      with open(f"archive/star/headlines", "w") as f:
        json.dump(headlines, f)