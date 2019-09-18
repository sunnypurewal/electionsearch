# -*- coding: utf-8 -*-
import scrapy


class GlobalSpider(scrapy.Spider):
  name = 'global'
  allowed_domains = ['global.ca']
  HOST = 'https://globalnews.ca/gnca-ajax/load-more/{"tag":"canada-election","last_id":"{0}"}/'
  last_id = 0

  def start_requests(self):
    url = self.HOST.format(self.last_id)
    print(url)
    return [scrapy.Request(url=url)]

  def parse(self, response):
    pass