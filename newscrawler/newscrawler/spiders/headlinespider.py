# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import os
import shutil

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
    headlines = []
    with open(f"{self.archivedir}/{self.name}/headlines.jsonc", "r") as f:
      fstring = f.read()
      if len(fstring) > 0:
        headlines.extend(json.loads(fstring))
    with open(f"{self.path}/{self.name}/headlines.jsonc", "r") as f:
      fstring = f.read()
      if len(fstring) > 0:
        headlines.extend(json.loads(fstring))
    with open(f"{self.archivedir}/{self.name}/headlines.jsonc", "w") as f:
      json.dump(headlines, f, default=lambda x: x.__dict__)
    for filename in os.listdir(f"{self.path}/{self.name}/articles"):
      shutil.move(f"{self.path}/{self.name}/articles/{filename}", 
                  f"{self.archivedir}/{self.name}/articles/{filename}")