# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlatvisualizerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source_id = scrapy.Field()
    link = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    size  = scrapy.Field()
    rooms = scrapy.Field()
    rent = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    time_to_work = scrapy.Field()