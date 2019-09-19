# -*- coding: utf-8 -*-
import scrapy
import json

class PostSpider(scrapy.Spider):
  HOST = 'https://nationalpost.com/category/news/politics/election-2019/page/{0}'
  name = 'post'
  allowed_domains = ['nationalpost.com']
  page = 2
  publisher = "post"

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url)]

  def parse(self, response):
    headlines = []
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
      headlines.append(headline)
    if len(headlines) > 0:
      print(len(headlines))
      with open(f"archive/{self.publisher}/headlines-{self.page-1}.jsonc", "w") as f:
        json.dump(headlines, f, default=lambda x: x.__dict__)
      self.page += 1
      return [scrapy.Request(url=self.HOST.format(self.page))]
