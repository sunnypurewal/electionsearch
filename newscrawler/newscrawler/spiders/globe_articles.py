# -*- coding: utf-8 -*-
import scrapy
import os
import json
import dateparser
import datetime
import articlespider

class GlobeArticlesSpider(articlespider.ArticleSpider):
  name = 'globe-articles'
  publisher = "globe"
  allowed_domains = ['theglobeandmail.com']

  def parse(self, response):
    paragraphs = response.css("p.c-article-body__text::text").getall()
    headline = response.meta["headline"]
    author = response.css(".c-byline::text").get()
    if author is not None:
      author = author.strip()
      headline["author"] = author
    id = headline["id"]
    tagstring = response.xpath("//head/meta[@name='news_keywords']/@content").get()
    if tagstring is not None:
      tags = []
      for tag in tagstring.split(","):
        tags.append(tag.strip())
      headline["tags"] = tags
    datestring = response.xpath("//head/meta[@property='article:published_time']/@content").get()
    headline["timestamp"] = dateparser.parse(datestring).timestamp()
    idx = -1
    for i, h in enumerate(self.headlines):
        if h["id"] == headline["id"]:
          idx = i
          break
    if idx != -1:
      self.headlines[idx] = headline
    self.save_article(id, paragraphs)