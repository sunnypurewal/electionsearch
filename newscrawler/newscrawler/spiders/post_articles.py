# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime
import articlespider

class PostArticlesSpider(articlespider.ArticleSpider):
  name = 'post-articles'
  publisher = "post"
  allowed_domains = ['nationalpost.com']
  headlines = []

  def parse(self, response):
    paragraphs = response.xpath("//div[@class='story-content']/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    datestring = response.xpath("//head/meta[@property='article:published_time']/@content").get()
    headline["timestamp"] = dateparser.parse(datestring).timestamp()
    tags = []
    for tag in response.xpath("//head/meta[@name='news_keywords']/@content").get().split(","):
      tags.append(tag.strip())
    headline["tags"] = tags
    idx = -1
    for i, h in enumerate(self.headlines):
      if h["id"] == headline["id"]:
        idx = i
        break
    if idx != -1:
      self.headlines[idx] = headline
    self.save_article(id, paragraphs)