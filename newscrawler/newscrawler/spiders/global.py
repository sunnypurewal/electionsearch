# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider
from headline import Headline
import dateparser
import datetime

class GlobalSpider(headlinespider.HeadlineSpider):
  name = 'global'
  allowed_domains = ['globalnews.ca']
  HOST = 'https://globalnews.ca/gnca-ajax/load-more/%7B%22tag%22%3A%22canada-election%22%2C%22last_id%22%3A%22{0}%22%7D/'
  last_id = 0
  page = 1

  def start_requests(self):
    url = self.HOST.format(self.last_id)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    stories = response.css("div.story")
    for story in stories:
      headline = Headline()
      article = story.css("article")
      a = story.css("h3.story-h").xpath("a")
      headline["url"] = a.xpath("@href").get()
      headline["title"] = a.xpath("text()").get()
      headline["title2"] = article.css("div.story-txt").css("p::text").get()
      headline["id"] = story.xpath("@data-post_id").get()
      headline["imgurl"] = article.css("img.story-img").xpath("@src").get()
      self.last_id = int(headline["id"])
      if self.should_get_article(headline["id"]):
        yield scrapy.Request(url=headline["url"],meta={"dont_cache":self.dont_cache,"headline":headline},callback=self.parse_body)
    url = self.HOST.format(self.last_id)
    yield scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})
    
  def parse_body(self, response):
    paragraphs = response.css("span.gnca-article-story-txt").xpath("p/text()").getall()
    headline = response.meta["headline"]
    id = headline["id"]
    tagstring = response.xpath("//body/meta[@name='news_keywords']/@content").get()
    headline["tags"] = tagstring.split(",")
    datestring = response.xpath("//head/meta[@name='pubdate']/@content").get()
    date = dateparser.parse(datestring)
    headline["timestamp"] = date.timestamp()
    if self.save_article(id, paragraphs):
      return headline