# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime
import articlespider

class HeraldArticlesSpider(articlespider.ArticleSpider):
  name = 'herald-articles'
  publisher = "herald"
  allowed_domains = ['calgaryherald.com']
  headlines = []

  def parse(self, response):
    paragraphs = response.xpath("//div[@itemprop='articleBody']/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
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
    self.save_article(id, paragraphs)