# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class HospitalFamilyItem(scrapy.Item):
    # define the fields for your item here like:
    PROVINCE = scrapy.Field()
    CITY = scrapy.Field()
    DISTRICT = scrapy.Field()
    HOSPITAL_NAME = scrapy.Field()

    NUM = scrapy.Field()

    ALIAS = scrapy.Field()
    POINT_LAT = scrapy.Field()
    POINT_LNG = scrapy.Field()
    ADDRESS = scrapy.Field()
    TEL = scrapy.Field()
    TYPE = scrapy.Field()
    RATE = scrapy.Field()
    LINK = scrapy.Field()
    IS_HOS = scrapy.Field()
    NATURE = scrapy.Field()



