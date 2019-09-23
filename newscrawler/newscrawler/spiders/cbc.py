# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider

class CBCSpider(headlinespider.HeadlineSpider):
  HOST = 'https://www.cbc.ca/aggregate_api/v1/items?typeSet=cbc-ocelot&pageSize=28&page={0}&lineupSlug=news-politics&categorySlug=empty-category&source=polopoly'
  name = 'cbc'
  allowed_domains = ['cbc.ca']
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    jsonresponse = json.loads(response.body_as_unicode())
    for item in jsonresponse:
      headline = {}
      headline["title"] = item["title"]
      headline["title2"] = item["typeAttributes"]["deck"]
      headline["description"] = item["description"]
      headline["url"] = item["typeAttributes"]["url"]
      headline["imageurl"] = item["typeAttributes"]["imageLarge"]
      headline["tags"] = item["typeAttributes"]["urlSlug"].split("-")
      headline["score"] = item["typeAttributes"]["trending"]["numViewers"]
      headline["timestamp"] = item["updatedAt"]
      headline["id"] = item["id"]
      self.headlines.append(headline)
    self.page += 1
    if self.page < 10:
      return [scrapy.Request(url=self.HOST.format(self.page),meta={"dont_cache":self.dont_cache})]
