# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import Hospital99Item

#
class InfoSpider(RedisSpider):
    name = 'hos99_slave'
    redis_key = 'hos99_spider:slave_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 解析编号NUM
        a = re.findall(r'/([a-z]+)/', response.url)[0]
        b = re.findall(r'/(\d +) /', response.url)[0]
        num = a + b
        con = response.xpath("//div[@class='hpi_content clearbox']")

        item = Hospital99Item()
        item['LINK'] = response.url
        item['HOS_NAME'] = response.xpath("//div[@class='hospital_name clearbox']/h1/text()").extract()[0].strip()
        item['ALIAS'] = con.xpath("ul/li[1]/span/text()").extract()[0]
        item['ADDRESS'] = con.xpath("ul/li[5]/span/text()").extract()[0]
        item['TEL'] = con.xpath("ul/li[4]/span/text()").extract()[0]
        item['RATE'] = con.xpath("ul/li[3]/span/text()").extract()[0]
        item['NATURE'] = con.xpath("ul/li[2]/span/text()").extract()[0]
        item["NUM"] = num

        yield item