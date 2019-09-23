# -*- coding: utf-8 -*-
import scrapy
import random
import json
import headlinespider
from headline import Headline
import dateparser
import datetime

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
      headline = Headline()
      a = story.xpath("div[@class='story__body']/span/span/a")
      url = f"https://www.thestar.com{a.xpath('@href').get()}"
      title = a.xpath("span[@class='story__headline']/text()").get()
      title2 = a.xpath("p[@class='story__abstract']/text()").get()
      headline["url"] = url
      headline["title"] = title
      headline["title2"] = title2
      headline["id"] = url.split("/")[-1].split(".")[0]
      if self.should_get_article(headline["id"]):
        yield scrapy.Request(url=headline["url"],meta={"dont_cache":self.dont_cache,"headline":headline},callback=self.parse_body)

  def parse_body(self, response):
    paragraphs = response.xpath("//div[@class='main-content']/p[@class='text-block-container']/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    tagstring = response.xpath("//meta[@name='news_keywords']/@content").get()
    headline["tags"] = tagstring.split(",")
    datestring = response.css("span.article__published-date::text").get()
    if datestring is not None:
      date = dateparser.parse(datestring)
      headline["timestamp"] = date.timestamp()
    if self.save_article(id, paragraphs):
      return headline