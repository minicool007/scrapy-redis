# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import AnjukeXiaoquItem
from scrapy_redis.spiders import RedisSpider
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class InfoSpider(RedisSpider):
    name = 'xzRecycle_slave'
    redis_key = 'xzRecycle_spider:slave_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        num = re.findall(r'(\d+)',response.url)[0]

        data = response.text.encode("utf-8")
        pattern1 = re.compile(r'lat : "(.*?)"')
        pattern2 = re.compile(r'lng : "(.*?)"')

        lat = pattern1.findall(data)[0]
        lng = pattern2.findall(data)[0]

        address = response.xpath("//div[@class='comm-title']/h1/span/text()").extract()[0]

        blocks = response.xpath("//*[@id='basic-infos-box']/dl/dd")
        manage_type = blocks[0].xpath("text()").extract()[0]
        manage_fee = blocks[1].xpath("text()").extract()[0]
        build_area = blocks[2].xpath("text()").extract()[0]
        build_year = blocks[4].xpath("text()").extract()[0]
        park = blocks[5].xpath("text()").extract()[0]
        volum = blocks[6].xpath("text()").extract()[0]
        green = blocks[7].xpath("text()").extract()[0]
        developer = blocks[8].xpath("text()").extract()[0]
        manage_company = blocks[9].xpath("text()").extract()[0]

        item = AnjukeXiaoquItem()
        item["NUM"] = num
        item['RES_ID'] = num
        item['ADDRESS'] = address.encode("utf-8").split("-")[2]
        item['POINT'] = lng + "," + lat
        item['BUILD_YEAR'] = build_year.encode("utf-8")
        item['MANAGE_TYPE'] = manage_type.encode("utf-8")
        item['MANAGE_COMPANY'] = manage_company.encode("utf-8")
        item['MANAGE_FEE'] = manage_fee.encode("utf-8")
        item['BUILD_AREA'] = build_area.encode("utf-8")
        item['GREEN'] = green.encode("utf-8")
        item['VOLUM'] = volum.encode("utf-8")
        item['DEVELOPER'] = developer.encode("utf-8")
        item['PARK'] = park.encode("utf-8")
        item['LINK'] = response.url

        url = "https://xuzhou.anjuke.com/v3/ajax/communityext/?commid=%s&useflg=onlyForAjax" % num
        yield scrapy.Request(url, meta={"item_meta":item},callback=self.parse_detail)
    def parse_detail(self,response):
        item = response.meta["item_meta"]

        # 解析房源数
        data = json.loads(response.text)
        house_num = str(data["comm_propnum"]["saleNum"]) + "套"
        rent_num = str(data["comm_propnum"]["rentNum"]) + "套"

        item_1 = AnjukeXiaoquItem()
        item_1['NUM'] = item["NUM"]
        item_1['RES_ID'] = item["NUM"]
        item_1['ADDRESS'] = item['ADDRESS']
        item_1['POINT'] = item['POINT']
        item_1['BUILD_YEAR'] = item['BUILD_YEAR']
        item_1['MANAGE_TYPE'] = item['MANAGE_TYPE']
        item_1['MANAGE_COMPANY'] = item['MANAGE_COMPANY']
        item_1['MANAGE_FEE'] = item['MANAGE_FEE']
        item_1['BUILD_AREA'] = item['BUILD_AREA']
        item_1['GREEN'] = item['GREEN']
        item_1['VOLUM'] = item['VOLUM']
        item_1['DEVELOPER'] = item['DEVELOPER']
        item_1['PARK'] = item['PARK']
        item_1['HOUSE_NUME'] = house_num
        item_1['RENT_NUM'] = rent_num
        item_1['LINK'] = item['LINK']
        yield item_1
