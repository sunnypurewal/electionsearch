# -*- coding: utf-8 -*-
import scrapy
import random
import json
import headlinespider

class StarSpider(headlinespider.HeadlineSpider):
  name = 'star'
  allowed_domains = ['thestar.com']
  HOST = 'https://www.thestar.com/news/federal-election.html'
  domain = 'https://www.thestar.com'

  def start_requests(self):
    return [scrapy.Request(url=self.HOST,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    stories = response.css(".story")
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
      self.headlines.append(headline)