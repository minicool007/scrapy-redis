# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeXzItem(scrapy.Item):
    # define the fields for your item here like:
    CITY = scrapy.Field() # 城市
    RES_NAME = scrapy.Field() # 楼盘名称
    DISTRICT = scrapy.Field() # 区域位置

    NUM = scrapy.Field() # 唯一标识

    RES_ID = scrapy.Field()  # 楼盘id
    POINT = scrapy.Field() # 经纬度坐标
    ADRESS = scrapy.Field() # 楼盘地址
    MANAGE_COMPANY = scrapy.Field() # 物业公司
    MANAGE_FEE = scrapy.Field() # 物业管理费
    BUILD_AREA = scrapy.Field() # 总建筑面积
    GREEN = scrapy.Field() # 绿化率
    VOLUM = scrapy.Field() # 容积率
    DEVELOPER = scrapy.Field() # 开发商
    NEW_SALE = scrapy.Field() # 最新开盘
    SUCCESS_TIME = scrapy.Field()  # 交盘时间
    PARK_NUM = scrapy.Field() # 车位数
    PARK_RATE = scrapy.Field() # 车位比
    USED_TIME = scrapy.Field() # 产权年限
    MANAGE_TYPE = scrapy.Field() # 物业类型
    BUILD_TYPE = scrapy.Field() # 建筑类型
    PLAN_NUM = scrapy.Field() # 规划户数
    STATE = scrapy.Field() # 楼层状况
    PROCCEED = scrapy.Field() # 工程进度
    LINK = scrapy.Field() # 小区URL
