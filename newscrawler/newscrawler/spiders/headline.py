import scrapy

class Headline(scrapy.Item):
  title = scrapy.Field()
  title2 = scrapy.Field()
  description = scrapy.Field()
  url = scrapy.Field()
  imgurl = scrapy.Field()
  tags = scrapy.Field()
  score = scrapy.Field()
  timestamp = scrapy.Field()
  author = scrapy.Field()
  id = scrapy.Field()