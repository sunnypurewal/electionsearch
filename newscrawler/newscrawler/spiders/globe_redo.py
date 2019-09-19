# -*- coding: utf-8 -*-
import scrapy
import json
import os

class GlobeRedoSpider(scrapy.Spider):
  # HOST = 'https://www.theglobeandmail.com/pb/api/v2/render/feature/global/story-feed?wrap=false&service=story-feed-query&contentConfig={"q":"taxonomy.seo_keywords%3A%22Federal%20Election%22%20AND%20NOT%20taxonomy.seo_keywords%3A%22United%20States%22%20AND%20NOT%20taxonomy.seo_keywords%3A%22U.S.%22","from":"{0}","size":"26"}&customFields={"linkTrackFeatureItemsContainerName":"view more articles","end":"20","listDisplayType":"standard","showSectionTitle":false,"loadMore":true,"noInlineAds":true,"feedType":"automatedFeed"}'
  FETCH_HOST = 'https://www.theglobeandmail.com/pb/api/v2/render/feature/global/story-feed?wrap=false&service=story-feed-query&contentConfig=%7B%22q%22%3A%22taxonomy.seo_keywords%253A%2522Federal%2520Election%2522%2520AND%2520NOT%2520taxonomy.seo_keywords%253A%2522United%2520States%2522%2520AND%2520NOT%2520taxonomy.seo_keywords%253A%2522U.S.%2522%22%2C%22from%22%3A%22{0}%22%2C%22size%22%3A%2210%22%7D&customFields=%7B%22linkTrackFeatureItemsContainerName%22%3A%22view%20more%20articles%22%2C%22end%22%3A%2220%22%2C%22listDisplayType%22%3A%22standard%22%2C%22showSectionTitle%22%3Afalse%2C%22loadMore%22%3Atrue%2C%22noInlineAds%22%3Atrue%2C%22feedType%22%3A%22automatedFeed%22%7D'
  HOST = "https://www.theglobeandmail.com"
  name = 'globe-redo'
  allowed_domains = ['theglobeandmail.com']
  last_id = 0
  publisher = "globe"
  headlines = []
  index = 0

  def start_requests(self):
    paths = []
    for filename in (os.listdir(f"archive/{self.publisher}")):
      if filename.find("headlines") == -1: continue
      path = f"archive/{self.publisher}/{filename}"
      if os.path.isdir(path): continue
      paths.append(path)
    paths.sort()
    for path in paths:
      with open(path, "r") as f:
        items = json.load(f)
        self.headlines.extend(items)
    url = self.FETCH_HOST.format(self.last_id)
    return [scrapy.Request(url=url)]

  def parse(self, response):
    html = json.loads(response.body_as_unicode())["rendering"]
    res = scrapy.http.HtmlResponse(url=response.url, body=html, encoding="utf-8")
    stories = res.css("div.c-card>a")
    for story in stories:
      time = int(story.css("time").xpath("@data-unixtime").get())
      self.headlines[self.index]["timestamp"] = time
      self.index += 1
    with open(f"archive/{self.publisher}/headlines-{int(self.last_id/10+1)}", "w") as f:
      json.dump(self.headlines[self.last_id:self.last_id+9], f)
    self.last_id += 10
    if self.last_id > 80:
      return scrapy.Request(url="")
    else:
      return scrapy.Request(url=self.FETCH_HOST.format(self.last_id))