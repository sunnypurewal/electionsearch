# -*- coding: utf-8 -*-
import scrapy
import json

class HeraldSpider(scrapy.Spider):
  name = 'herald'
  allowed_domains = ['calgaryherald.com']
  HOST = 'https://calgaryherald.com/category/news/politics/election-2019/page/{0}'
  page = 1
  publisher = "herald"
  headlines = []

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url)]

  def parse(self, response):
    stories = response.css("article.post")
    for story in stories:
      headline = {}
      headline["url"] = story.css(".entry-title>a").xpath("@href").get()
      headline["title"] = story.css(".entry-title>a::text").get()
      data = json.loads(story.xpath("@data-evt-val").get())
      headline["id"] = data["story"]["id"] if data["story"]["id"] else headline["url"].split("/")[-1]
      print (headline["id"])
      headline["imgurl"] = story.css("img.attachment-post-thumbnail").xpath("@src").get()
      self.headlines.append(headline)
    if len(self.headlines) > 0:
      print(len(self.headlines))
      with open(f"archive/{self.publisher}/headlines.jsonc", "w") as f:
        json.dump(self.headlines, f, default=lambda x: x.__dict__)
      # self.page += 1
      # if self.page <= 10:
        # return scrapy.Request(url=self.HOST.format(self.page))
    