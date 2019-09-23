# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider
from headline import Headline
import dateparser
import datetime

class HeraldSpider(headlinespider.HeadlineSpider):
  name = 'herald'
  allowed_domains = ['calgaryherald.com']
  HOST = 'https://calgaryherald.com/category/news/politics/election-2019/page/{0}'
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.page)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    stories = response.css("article.post")
    for story in stories:
      headline = Headline()
      headline["url"] = story.css(".entry-title>a").xpath("@href").get()
      headline["title"] = story.css(".entry-title>a::text").get()
      data = json.loads(story.xpath("@data-evt-val").get())
      headline["id"] = data["story"]["id"] if data["story"]["id"] else headline["url"].split("/")[-1]
      headline["imgurl"] = story.css("img.attachment-post-thumbnail").xpath("@src").get()
      if self.should_get_article(headline["id"]):
        yield scrapy.Request(url=headline["url"],meta={"dont_cache":self.dont_cache,"headline":headline},callback=self.parse_body)
    # self.page += 1
    # if self.page <= 10:
      # return scrapy.Request(url=self.HOST.format(self.page))
    
  def parse_body(self, response):
    paragraphs = response.xpath("//div[@itemprop='articleBody']/p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    datestring = response.xpath("//head/meta[@property='article:published_time']/@content").get()
    headline["timestamp"] = dateparser.parse(datestring).timestamp()
    headline["author"] = response.xpath("//div[@class='author-wrap']/span[@class='name']/text()").get()
    tagstring = response.xpath("//meta[@name='news_keywords']/@content").get()
    if tagstring is not None:
      headline["tags"] = tagstring.split(",")
    if self.save_article(id, paragraphs):
      return headline