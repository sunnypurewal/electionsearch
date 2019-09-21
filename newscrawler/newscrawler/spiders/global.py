# -*- coding: utf-8 -*-
import scrapy
import json

class GlobalSpider(scrapy.Spider):
  name = 'global'
  allowed_domains = ['globalnews.ca']
  HOST = 'https://globalnews.ca/gnca-ajax/load-more/%7B%22tag%22%3A%22canada-election%22%2C%22last_id%22%3A%22{0}%22%7D/'
  last_id = 0
  page = 1
  publisher = "global"
  headlines = []

  def start_requests(self):
    url = self.HOST.format(self.last_id)
    return [scrapy.Request(url=url,meta={"dont_cache":True})]

  def parse(self, response):
    stories = response.css("div.story")
    for story in stories:
      headline = {}
      article = story.css("article")
      a = story.css("h3.story-h").xpath("a")
      headline["url"] = a.xpath("@href").get()
      headline["title"] = a.xpath("text()").get()
      headline["title2"] = article.css("div.story-txt").css("p::text").get()
      headline["id"] = story.xpath("@data-post_id").get()
      headline["imgurl"] = article.css("img.story-img").xpath("@src").get()
      self.last_id = int(headline["id"])
      self.headlines.append(headline)
    if len(self.headlines) > 0:
      print(len(self.headlines))
      with open(f"archive/{self.publisher}/headlines.jsonc", "w") as f:
        json.dump(self.headlines, f, default=lambda x: x.__dict__)
      url = self.HOST.format(self.last_id)
      return scrapy.Request(url=url,meta={"dont_cache":True})
    