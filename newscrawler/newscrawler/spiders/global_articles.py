# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime
import articlespider

class GlobalArticlesSpider(articlespider.ArticleSpider):
  name = 'global-articles'
  allowed_domains = ['globalnews.ca']
  HOST = "https://globalnews.ca"

  def parse(self, response):
    paragraphs = response.css("span.gnca-article-story-txt").xpath("p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    tagstring = response.xpath("//body/meta[@name='news_keywords']/@content").get()
    headline["tags"] = tagstring.split(",")
    datestring = response.xpath("//head/meta[@name='pubdate']/@content").get()
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