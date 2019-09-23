# -*- coding: utf-8 -*-
import scrapy
import json

class HillTimesSpider(scrapy.Spider):
  name = 'hilltimes'
  allowed_domains = ['hilltimes.com']
  HOST = 'https://www.hilltimes.com/election-2019'
  last_id = 0
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.last_id)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    stories = response.css(".storyBox")
    for story in stories:
      headline = {}
      headline["url"] = story.css(".htitle3,.htitle8").xpath("a/@href").get()
      headline["title"] = story.css(".htitle3,.htitle8").xpath("a/text()").get()
      headline["title2"] = story.css(".hexcerpt::text").get()
      headline["author"] = story.css(".hauthor").css("a::text").get()
      headline["id"] = story.css(".htitle3,.htitle8").xpath("a/@href").get().split("/")[-1]
      headline["imgurl"] = story.css("a>img").xpath("@src").get()
      yield headline