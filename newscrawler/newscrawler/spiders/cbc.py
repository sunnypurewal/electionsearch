# -*- coding: utf-8 -*-
import scrapy
import json
from headline import Headline


class CbcSpider(scrapy.Spider):
  HOST = 'https://www.cbc.ca/aggregate_api/v1/items?typeSet=cbc-ocelot&pageSize=28&page={0}&lineupSlug=news-politics&categorySlug=empty-category&source=polopoly'
  name = 'cbc'
  allowed_domains = ['cbc.ca']
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url)]

  def parse(self, response):
    jsonresponse = json.loads(response.body_as_unicode())
    headlines = []
    for item in jsonresponse:
      headline = Headline()
      headline.title = item["title"]
      headline.title2 = item["typeAttributes"]["deck"]
      headline.description = item["description"]
      headline.url = item["typeAttributes"]["url"]
      headline.imageurl = item["typeAttributes"]["imageLarge"]
      headline.tags = item["typeAttributes"]["urlSlug"].split("-")
      headline.score = item["typeAttributes"]["trending"]["numViewers"]
      headline.timestamp = item["updatedAt"]
      headline.id = item["id"]
      headlines.append(headline)
    if len(jsonresponse) > 0:
      with open(f"archive/cbc-{self.page}", "w") as f:
        json.dump(headlines, f, default=lambda x: x.__dict__)
      self.page += 1
      return [scrapy.Request(url=self.HOST.format(self.page))]
