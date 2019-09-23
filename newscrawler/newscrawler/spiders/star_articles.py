# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime
import articlespider

class StarArticlesSpider(articlespider.ArticleSpider):
  name = 'star-articles'
  publisher = "star"
  allowed_domains = ['thestar.com']
  HOST = "https://www.thestar.com"
  headlines = []
  
  def parse(self, response):
    paragraphs = response.xpath("//div[@class='main-content']/p[@class='text-block-container']/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    tagstring = response.xpath("//meta[@name='news_keywords']/@content").get()
    headline["tags"] = tagstring.split(",")
    datestring = response.css("span.article__published-date::text").get()
    if datestring is not None:
      date = dateparser.parse(datestring)
      headline["timestamp"] = date.timestamp()
    idx = -1
    for i, h in enumerate(self.headlines):
      if h["id"] == headline["id"]: 
        idx = i
        break
    if idx != -1:
      self.headlines[idx] = headline
    self.save_article(id, paragraphs)