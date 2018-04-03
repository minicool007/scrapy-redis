# -*- coding: utf-8 -*-
import scrapy
import re
import scrapy
from redis import Redis
from ..items import Hospital99Item
from scrapy_redis.spiders import RedisSpider
# lpush hos99_spider:master_urls http://yyk.99.com.cn
class Hos99Spider(RedisSpider):
    name = 'hos99_master'
    redis_key = 'hos99_spider:master_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Hos99Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = []
        pros = response.xpath("//div[@class='lcr_bottom']/ul/li/a")
        base_url = "http://yyk.99.com.cn"
        for pro in pros:
            url = base_url + pro.xpath("@href").extract()[0].encode("utf-8")
            pro_name = pro.xpath("text()").extract()[0]

            item = Hospital99Item()
            item["PROVINCE"] = pro_name.strip()

            data = {"url": url, "item_meta": item}
            data_list.append(data)
        for data in data_list:
            yield scrapy.Request(data["url"], meta={'item_meta': data['item_meta']}, callback=self.parse_city,dont_filter=True)

    def parse_city(self, response):
        item = response.meta['item_meta']

        data_list = []
        citys = response.xpath("//div[@class='fontlist']/ul/li/a")
        for city in citys:
            url = city.xpath("@href").extract()[0]
            city_name = city.xpath("text()").extract()[0]

            item_1 = Hospital99Item()
            item_1["CITY"] = city_name.strip()
            item_1["PROVINCE"] = item["PROVINCE"]

            data = {"url": url, "item_meta": item_1}
            data_list.append(data)
        for data in data_list:
            yield scrapy.Request(data["url"], meta={'item_meta': data['item_meta']}, callback=self.parse_district,dont_filter=True)

    def parse_district(self, response):
        item = response.meta['item_meta']

        block = response.xpath("//div[@class='area_list']/div[@class='fontlist']/h3")
        if len(block) == 0:
            # 只有两层
            hos_s = response.xpath("//div[@class='area_list']/div/ul/li/a")
            for hos in hos_s:
                hoa_name = hos.xpath("@title").extract()[0]
                url = hos.xpath("@href").extract()[0]
                a = re.findall(r'cn/(.*?)/', url)[0]
                b = re.findall(r'/(\d+)/', url)[0]

                item_1 = Hospital99Item()
                item_1["HOS_NAME"] = hoa_name.strip()
                item_1["DISTRICT"] = item["CITY"]
                item_1["CITY"] = item["PROVINCE"]
                item_1["PROVINCE"] = item["PROVINCE"]
                item_1["NUM"] = a + b
                self.r.lpush("hos99_spider:slave_urls", url)
                yield item_1
        else:
            # 继续解析
            data_list = []
            districts = response.xpath("//div[@class='fontlist']/ul/li")
            for dis in districts:
                url = dis.xpath("a/@href").extract()[0]
                dis_name = dis.xpath("a/text()").extract()[0]

                item_1 = Hospital99Item()
                item_1["DISTRICT"] = dis_name.strip()
                item_1["CITY"] = item["CITY"]
                item_1["PROVINCE"] = item["PROVINCE"]

                data = {"url": url, "item_meta": item_1}
                data_list.append(data)
            for data in data_list:
                yield scrapy.Request(data["url"], meta={'item_meta': data['item_meta']}, callback=self.parse_page,dont_filter=True)

    def parse_page(self, response):
        item = response.meta['item_meta']

        hos_s = response.xpath("//div[@class='area_list']/div/ul/li/a")
        for hos in hos_s:
            try:
                hoa_name = hos.xpath("@title").extract()[0]
            except:
                continue
            url = hos.xpath("@href").extract()[0]
            a = re.findall(r'cn/(.*?)/', url)[0]
            b = re.findall(r'/(\d+)/', url)[0]

            item_1 = Hospital99Item()
            item_1["HOS_NAME"] = hoa_name.strip()
            item_1["DISTRICT"] = item["DISTRICT"]
            item_1["CITY"] = item["CITY"]
            item_1["PROVINCE"] = item["PROVINCE"]
            item_1["NUM"] = a + b
            self.r.lpush("hos99_spider:slave_urls", url)
            yield item_1

