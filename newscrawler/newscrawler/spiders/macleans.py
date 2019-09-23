# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider
from headline import Headline
import dateparser
import datetime

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
      headline = Headline()
      headline["url"] = story.css("div.row>div.text>header>a").xpath("@href").get()
      headline["title"] = story.css("div.row>div.text>header>a").xpath("@title").get()
      headline["title2"] = story.css("div.row>div.text>header>a>div.excerpt>p::text").get()
      headline["id"] = story.xpath("@id").get().split("-")[-1]
      headline["imgurl"] = story.css("img").xpath("@data-src").get()
      if self.should_get_article(headline["id"]):
        yield scrapy.Request(url=headline["url"],meta={"dont_cache":self.dont_cache,"headline":headline},callback=self.parse_body)
    self.page += 1
    if self.page <= 10:
      yield scrapy.Request(url=self.HOST.format(self.page),meta={"dont_cache":self.dont_cache})
    
  def parse_body(self, response):
    paragraphs = response.css("span.entry-content>p::text").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    datestring = response.css("p.entry-date").xpath("@content").get()
    if datestring is not None:
      date = dateparser.parse(datestring)
      headline["timestamp"] = date.timestamp()
    headline["author"] = response.css("span.authorName>span>a::text").get()
    if self.save_article(id, paragraphs):
      return headline