# -*- coding: utf-8 -*-
import scrapy
import json
import headlinespider

class GlobeSpider(headlinespider.HeadlineSpider):
  # HOST = 'https://www.theglobeandmail.com/pb/api/v2/render/feature/global/story-feed?wrap=false&service=story-feed-query&contentConfig={"q":"taxonomy.seo_keywords%3A%22Federal%20Election%22%20AND%20NOT%20taxonomy.seo_keywords%3A%22United%20States%22%20AND%20NOT%20taxonomy.seo_keywords%3A%22U.S.%22","from":"{0}","size":"26"}&customFields={"linkTrackFeatureItemsContainerName":"view more articles","end":"20","listDisplayType":"standard","showSectionTitle":false,"loadMore":true,"noInlineAds":true,"feedType":"automatedFeed"}'
  FETCH_HOST = 'https://www.theglobeandmail.com/pb/api/v2/render/feature/global/story-feed?wrap=false&service=story-feed-query&contentConfig=%7B%22q%22%3A%22taxonomy.seo_keywords%253A%2522Federal%2520Election%2522%2520AND%2520NOT%2520taxonomy.seo_keywords%253A%2522United%2520States%2522%2520AND%2520NOT%2520taxonomy.seo_keywords%253A%2522U.S.%2522%22%2C%22from%22%3A%22{0}%22%2C%22size%22%3A%2210%22%7D&customFields=%7B%22linkTrackFeatureItemsContainerName%22%3A%22view%20more%20articles%22%2C%22end%22%3A%2220%22%2C%22listDisplayType%22%3A%22standard%22%2C%22showSectionTitle%22%3Afalse%2C%22loadMore%22%3Atrue%2C%22noInlineAds%22%3Atrue%2C%22feedType%22%3A%22automatedFeed%22%7D'
  HOST = "https://www.theglobeandmail.com"
  name = 'globe'
  allowed_domains = ['theglobeandmail.com']
  last_id = 0

  def start_requests(self):
    url = self.FETCH_HOST.format(self.last_id)
    return [scrapy.Request(url=url,meta={"dont_cache":self.dont_cache})]

  def parse(self, response):
    html = json.loads(response.body_as_unicode())["rendering"]
    res = scrapy.http.HtmlResponse(url=response.url, body=html, encoding="utf-8")
    stories = res.css("div.c-card>a")
    for story in stories:
      url = f"{self.HOST}{story.xpath('@href').get()}"
      id = url.split("/")[-2]
      author = story.css("span.c-card__author::text").get()
      title = story.css("div.c-card__hed-text::text").get()
      imgurl = story.css("img.c-image").xpath("@src").get()
      headline = {
        "id": id,
        "url": url,
        "author": author,
        "title": title,
        "imgurl": imgurl
      }
      self.headlines.append(headline)
    self.last_id += 10
    if self.last_id > 80:
      return scrapy.Request(url="")
    else:
      return scrapy.Request(url=self.FETCH_HOST.format(self.last_id),meta={"dont_cache":self.dont_cache})