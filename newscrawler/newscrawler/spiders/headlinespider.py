# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import os
import shutil
from elasticsearch import Elasticsearch

class HeadlineSpider(scrapy.Spider):
  def __init__(self, domain="", *args, **kwargs):
    self.path = kwargs["path"]
    self.dont_cache = kwargs["dont_cache"]
    self.archivedir = kwargs["archivedir"]
    logging.getLogger("scrapy").propagate = False

  def save_article(self, id, paragraphs):
    if len(paragraphs) == 0: 
      return False
    with open(f"{self.path}/{self.name.split('-')[0]}/articles/{id}.txt", "w") as f:
      f.write("\n".join(paragraphs))
      return True
  
  def should_get_article(self, id):
    return not os.path.exists(f"{self.archivedir}/{self.name}/articles/{id}.txt")
  
  def closed(self, reason):
    es = Elasticsearch()
    headlines = []
    if os.path.exists(f"{self.archivedir}/{self.name}/headlines.jsonc"):
      with open(f"{self.archivedir}/{self.name}/headlines.jsonc", "r") as f:
        fstring = f.read()
        if len(fstring) > 0:
          headlines.extend(json.loads(fstring))
    with open(f"{self.path}/{self.name}/headlines.jsonc", "r") as f:
      fstring = f.read()
      if len(fstring) > 0:
        tmp = json.loads(fstring)
        for h in tmp:
          if not "timestamp" in h: continue
          with open(f"{self.path}/{self.name}/articles/{h['id']}.txt", "r") as f2:
            h["body"] = "\n".join(f2.readlines())
            h["timestamp"] = int(h["timestamp"]) if not self.name == "cbc" else int(h["timestamp"]/1000)
            es.index(index="articles",id=h["id"],body=h)
        headlines.extend(tmp)
    with open(f"{self.archivedir}/{self.name}/headlines.jsonc", "w") as f:
      json.dump(headlines, f, default=lambda x: x.__dict__)
    for filename in os.listdir(f"{self.path}/{self.name}/articles"):
      shutil.move(f"{self.path}/{self.name}/articles/{filename}", 
                  f"{self.archivedir}/{self.name}/articles/{filename}")