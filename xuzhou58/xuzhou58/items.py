# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Xuzhou58Item(scrapy.Item):
    # define the fields for your item here like:
    CITY = scrapy.Field() # 城市
    DISTRICT = scrapy.Field() # 商圈区域
    COMUNITY_NAME = scrapy.Field() # 小区名称
    ALIAS = scrapy.Field() #

    NUM =scrapy.Field()

    POINT = scrapy.Field() # 坐标
    ADDRESS = scrapy.Field() # 小区地址
    USED_TIME = scrapy.Field() # 产权年限
    TYPE = scrapy.Field() # 产权类别
    BUILD_TIME = scrapy.Field() # 建筑年代
    BUILD_TYPE = scrapy.Field() # 建筑类型
    MANAGE_COMPANY = scrapy.Field() # 物业公司
    MANAGE_FEE = scrapy.Field() # 物业费
    DEVELOPER = scrapy.Field() # 开发商
    BUILD_AREA = scrapy.Field() # 建筑面积
    AREA = scrapy.Field() # 占地面积
    GREEN = scrapy.Field() # 绿化率
    VOLUM = scrapy.Field() # 容积率
    PARK = scrapy.Field() # 车位信息
    DESCRIPTION = scrapy.Field() # 项目介绍
    HOUSE_NUM = scrapy.Field() # 二手房源数
    RENT_NUM = scrapy.Field() # 住房房源数
    LINK = scrapy.Field() # 小区url
    COM_ID = scrapy.Field()  # 小区id
