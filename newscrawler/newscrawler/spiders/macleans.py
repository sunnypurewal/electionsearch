# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider

class MacleansSpider(headlinespider.HeadlineSpider):
  name = 'macleans'
  allowed_domains = ['macleans.ca']
  HOST = 'https://www.macleans.ca/politics/page/{0}/'
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    stories = response.css("article.post")
    for story in stories:
      headline = {}
      headline["url"] = story.css("div.row>div.text>header>a").xpath("@href").get()
      headline["title"] = story.css("div.row>div.text>header>a").xpath("@title").get()
      headline["title2"] = story.css("div.row>div.text>header>a>div.excerpt>p::text").get()
      headline["id"] = story.xpath("@id").get().split("-")[-1]
      headline["imgurl"] = story.css("img").xpath("@data-src").get()
      self.headlines.append(headline)
    self.page += 1
    if self.page <= 10:
      return scrapy.Request(url=self.HOST.format(self.page),meta={"dont_cache":self.dont_cache})
    