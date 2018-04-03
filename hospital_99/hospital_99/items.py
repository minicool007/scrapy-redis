# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Hospital99Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PROVINCE = scrapy.Field()
    CITY = scrapy.Field()
    DISTRICT = scrapy.Field()
    HOS_NAME = scrapy.Field()
    LINK = scrapy.Field()

    NUM = scrapy.Field()

    ALIAS = scrapy.Field()
    ADDRESS = scrapy.Field()
    TEL = scrapy.Field()
    RATE = scrapy.Field()
    NATURE = scrapy.Field()
