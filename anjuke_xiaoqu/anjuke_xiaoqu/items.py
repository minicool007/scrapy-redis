# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeXiaoquItem(scrapy.Item):
    RES_NAME = scrapy.Field()
    DISTRICT = scrapy.Field()
    CITY = scrapy.Field()

    NUM = scrapy.Field()

    RES_ID = scrapy.Field()
    ADDRESS = scrapy.Field()
    POINT = scrapy.Field()
    BUILD_YEAR = scrapy.Field()
    MANAGE_TYPE = scrapy.Field()
    MANAGE_COMPANY = scrapy.Field()
    MANAGE_FEE = scrapy.Field()
    BUILD_AREA = scrapy.Field()
    GREEN = scrapy.Field()
    VOLUM = scrapy.Field()
    DEVELOPER = scrapy.Field()
    PARK = scrapy.Field()
    HOUSE_NUME = scrapy.Field()
    RENT_NUM = scrapy.Field()
    LINK = scrapy.Field()
