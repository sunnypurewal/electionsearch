# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider
from headline import Headline
import dateparser
import datetime

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
      headline = Headline()
      headline["title"] = item["title"]
      headline["title2"] = item["typeAttributes"]["deck"]
      headline["description"] = item["description"]
      headline["url"] = item["typeAttributes"]["url"]
      headline["imgurl"] = item["typeAttributes"]["imageLarge"]
      headline["tags"] = item["typeAttributes"]["urlSlug"].split("-")
      headline["score"] = item["typeAttributes"]["trending"]["numViewers"]
      headline["timestamp"] = item["updatedAt"]
      headline["id"] = item["id"]
      if self.should_get_article(headline["id"]):
        yield scrapy.Request(url=headline["url"],meta={"dont_cache":self.dont_cache,"headline":headline},callback=self.parse_body)
    self.page += 1
    if self.page < 10:
      yield scrapy.Request(url=self.HOST.format(self.page),meta={"dont_cache":self.dont_cache})

  def parse_body(self, response):
    paragraphs = response.xpath("//div[@class='story']/span/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    if self.save_article(id, paragraphs):
      return headline