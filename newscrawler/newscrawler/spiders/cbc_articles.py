# -*- coding: utf-8 -*-
import scrapy
import os
import json
import articlespider

class CbcArticlesSpider(articlespider.ArticleSpider):
  name = 'cbc-articles'
  allowed_domains = ['cbc.ca']
  publisher = "cbc"

  def parse(self, response):
    paragraphs = response.xpath("//div[@class='story']/span/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    self.save_article(id, paragraphs)
