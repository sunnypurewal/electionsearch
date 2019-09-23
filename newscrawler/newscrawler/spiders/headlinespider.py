# -*- coding: utf-8 -*-
import scrapy
import json
import logging

class HeadlineSpider(scrapy.Spider):
  def __init__(self, domain="", *args, **kwargs):
    self.path = kwargs["path"]
    self.dont_cache = kwargs["dont_cache"]
    logging.getLogger("scrapy").setLevel(5)
  page = 1
  headlines = []

  def parse(self, response):
    pass

  def closed(self, reason):
    if len(self.headlines) > 0:
      with open(f"{self.path}/{self.name}/headlines.jsonc", "w") as f:
        print(f"Writing out new headlines file for {self.name} with length {len(self.headlines)}")
        json.dump(self.headlines, f, default=lambda x: x.__dict__)