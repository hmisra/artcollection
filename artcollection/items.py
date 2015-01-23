# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtcollectionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    artist = scrapy.Field()
    artistlife = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    image = scrapy.Field()
    medium = scrapy.Field()
    dimensions = scrapy.Field()
    collection = scrapy.Field()
    acquisition = scrapy.Field()
    reference = scrapy.Field()
    info = scrapy.Field()
    artistbio = scrapy.Field()
