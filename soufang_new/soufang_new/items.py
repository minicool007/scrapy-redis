# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoufangNewItem(scrapy.Item):

    CITY = scrapy.Field()
    DISTRICT = scrapy.Field()
    RES_NAME = scrapy.Field()

    NUM = scrapy.Field()

    RES_ID = scrapy.Field()
    POINT = scrapy.Field()
    ADDRESS = scrapy.Field()
    MANAGE_TYPE = scrapy.Field()
    BUILD_TYPE = scrapy.Field()
    USED_YEAR = scrapy.Field()
    LOCATION = scrapy.Field()
    DEVELOPER = scrapy.Field()
    OPEN_TIME = scrapy.Field()
    SUCCESS_TIME = scrapy.Field()
    SALE_STATE = scrapy.Field()
    SALE_ADDRESS = scrapy.Field()
    MANAGE_COMPANY = scrapy.Field()
    MANAGE_FEE = scrapy.Field()
    MANAGE_DESC = scrapy.Field()
    BUILD_AREA = scrapy.Field()
    AREA = scrapy.Field()
    GREEN = scrapy.Field()
    VOLUM = scrapy.Field()
    PARK = scrapy.Field()
    BUILD_NUM = scrapy.Field()
    HOUSE_NUM = scrapy.Field()
    STATE = scrapy.Field()
    DESCRIPT = scrapy.Field()
    LINK = scrapy.Field()
