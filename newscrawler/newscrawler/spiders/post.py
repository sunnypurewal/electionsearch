# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider
from headline import Headline
import dateparser
import datetime

class PostSpider(headlinespider.HeadlineSpider):
  HOST = 'https://nationalpost.com/category/news/politics/election-2019/page/{0}'
  name = 'post'
  allowed_domains = ['nationalpost.com']
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    posts = response.css("article.post")
    for post in posts:
      headline = Headline()
      headline["title"] = post.css(".entry-title").xpath("a/text()").get()
      headline["title2"] = response.css("article.post").css(".entry-content::text").get().strip()
      headline["url"] = post.css(".entry-title").xpath("a/@href").get()
      imgsrc = post.css("figure.thumbnail").xpath("a/img/@src").get()
      imgsrc2 = post.css("figure.thumbnail").xpath("a/img/@pm-lazy-src").get()
      if imgsrc is not None and imgsrc.find("data:") == -1 and imgsrc.find("http") != -1:
        headline["imgurl"] = imgsrc
      elif imgsrc2 is not None and imgsrc2.find("http") != -1:
        headline["imgurl"] = imgsrc2
      headline["id"] = post.xpath("@data-event-tracking").get().split("|")[-2]
      if self.should_get_article(headline["id"]):
        yield scrapy.Request(url=headline["url"],meta={"dont_cache":False,"headline":headline},callback=self.parse_body)
    self.page += 1
    yield scrapy.Request(url=self.HOST.format(self.page),meta={"dont_cache":self.dont_cache})

  def parse_body(self, response):
    paragraphs = response.xpath("//div[@class='story-content']/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    datestring = response.xpath("//head/meta[@property='article:published_time']/@content").get()
    headline["timestamp"] = dateparser.parse(datestring).timestamp()
    tags = []
    for tag in response.xpath("//head/meta[@name='news_keywords']/@content").get().split(","):
      tags.append(tag.strip())
    headline["tags"] = tags
    if self.save_article(id, paragraphs):
      return headline