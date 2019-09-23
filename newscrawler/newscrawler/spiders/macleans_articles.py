# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime
import articlespider

class MacleansArticlesSpider(articlespider.ArticleSpider):
  name = 'macleans-articles'
  publisher = "macleans"
  allowed_domains = ['macleans.ca']
  HOST = "https://macleans.ca"
  headlines = []

  def parse(self, response):
    paragraphs = response.css("span.entry-content>p::text").getall()
    headline = response.meta["headline"]
    id = headline["id"]
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
    self.save_article(id, paragraphs)