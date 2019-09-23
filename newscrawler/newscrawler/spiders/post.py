# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider

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
      headline = {}
      headline["title"] = post.css(".entry-title").xpath("a/text()").get()
      headline["title2"] = response.css("article.post").css(".entry-content::text").get().strip()
      headline["url"] = post.css(".entry-title").xpath("a/@href").get()
      imgsrc = post.css("figure.thumbnail").xpath("a/img/@src").get()
      imgsrc2 = post.css("figure.thumbnail").xpath("a/img/@pm-lazy-src").get()
      if imgsrc is not None and imgsrc.find("data:") == -1 and imgsrc.find("http") != -1:
        headline["imageurl"] = imgsrc
      elif imgsrc2 is not None and imgsrc2.find("http") != -1:
        headline["imageurl"] = imgsrc2
      headline["id"] = post.xpath("@data-event-tracking").get().split("|")[-2]
      self.headlines.append(headline)
    self.page += 1
    return [scrapy.Request(url=self.HOST.format(self.page),meta={"dont_cache":self.dont_cache})]
