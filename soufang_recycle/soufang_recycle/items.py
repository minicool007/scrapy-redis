# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoufangRecycleItem(scrapy.Item):
    # define the fields for your item here like:
    CITY = scrapy.Field()
    RES_NAME = scrapy.Field()
    DISTRICT = scrapy.Field()

    NUM = scrapy.Field()

    RES_ID = scrapy.Field()
    POINT = scrapy.Field()
    ADDRESS = scrapy.Field()
    LOCATION = scrapy.Field()
    BUILD_YEAR = scrapy.Field()
    MANAGE_TYPE = scrapy.Field()
    DESCRIPTION = scrapy.Field()
    BUILD_STRUCTURE = scrapy.Field()
    BUILD_TYPE = scrapy.Field()
    MANAGE_COMPANY = scrapy.Field()
    MANAGE_LOCATION = scrapy.Field()
    MANAGE_TEL = scrapy.Field()
    MANAGE_FEE = scrapy.Field()
    INFO = scrapy.Field()
    BUILD_AREA = scrapy.Field()
    AREA = scrapy.Field()
    GREEN = scrapy.Field()
    VOLUM = scrapy.Field()
    DEVELOPER = scrapy.Field()
    OPEN_TIME = scrapy.Field()
    SUCCESS_TIME = scrapy.Field()
    PARK = scrapy.Field()
    SCHOOL = scrapy.Field()
    HOUSE_NUM = scrapy.Field()
    RENT_NUM = scrapy.Field()
    LINK = scrapy.Field()
