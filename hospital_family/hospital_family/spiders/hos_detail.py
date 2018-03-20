# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy_redis.spiders import RedisSpider
from ..items import HospitalFamilyItem

# lpush hospital_spider:slave2_urls https://yyk.familydoctor.com.cn/7/
class InfoSpider(RedisSpider):
    name = 'hospital_slave1'
    redis_key = 'hospital_spider:slave8_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 解析编号NUM
        num = re.findall(r'/(\d+)/', response.url)[0]
        # 判断是专科还是公立医院
        try:
            # 常规医院
            name = response.xpath("//div[@class='subLogo']/h1/text()").extract()[0]
            flag = 1
        except:
            flag = 2
        if flag == 1:
            # 别名 类型 等级 地址 坐标 电话 链接 https://yyk.familydoctor.com.cn/7/
            try:
                alias = response.xpath("//div[@class='subLogo']/strong/text()").extract()[0]
            except:
                alias = ""
            type = response.xpath("//div[@class='introPic']/dl[1]/dd/text()").extract()[0]
            rate = response.xpath("//div[@class='introPic']/dl[2]/dd/span/text()").extract()[0]
            address = response.xpath("//div[@class='introPic']/dl[3]/dd/text()").extract()[0]
            tel = response.xpath("//div[@class='introPic']/dl[4]/dd[1]/text()").extract()[0].strip()
            link = response.url

            item = HospitalFamilyItem()
            item['NUM'] = str(num)
            item['HOSPITAL_NAME'] = name
            item['ALIAS'] = alias
            item['ADDRESS'] = address
            item['TEL'] = tel
            item['TYPE'] = type
            item['RATE'] = rate
            item['LINK'] = link
            url = response.url+"/detail/"
            yield scrapy.Request(url, meta={ 'item_meta': item, 'flag': flag}, callback=self.parse_detail)
        else:
            name = response.xpath("//dl[@class='message']/dt/text()").extract()[0]

            addr = response.xpath("//dl[@class='message']/dd/p[1]/text()").extract()[0]
            x = addr + "-".decode('utf-8')
            address = x[5:-1]

            tl = response.xpath("//dl[@class='message']/dd/p[2]/text()").extract()[0]
            y = tl + "-".decode('utf-8')
            tel = y[5:-1]

            item = HospitalFamilyItem()
            item['NUM'] = str(num)
            item['ADDRESS'] = address
            item['TEL'] = tel
            item['LINK'] = response.url
            item['HOSPITAL_NAME'] = name
            item['TYPE'] = "专科医院"
            baidu_url = "https://api.map.baidu.com/?qt=gc&wd=%s&ie=utf-8&oue=1&fromproduct=jsapi&res=api&ak=BQhoozAa4tLcjRjiGqsFFA4X" % (item['ADDRESS'])
            yield scrapy.Request(baidu_url, meta={'item_meta': item, 'flag': flag}, callback=self.parse_point)

    def parse_detail(self, response):
        item = response.meta['item_meta']
        flag = response.meta['flag']

        is_hos = response.xpath("//div[@class='moduleContent']/dl[2]/dd/text()").extract()[0]
        nature = response.xpath("//div[@class='moduleContent']/dl[4]/dd/text()").extract()[0]

        item_1 = HospitalFamilyItem()
        item_1['IS_HOS'] = is_hos
        item_1['NATURE'] = nature

        item_1['NUM'] = item['NUM']
        item_1['HOSPITAL_NAME'] = item['HOSPITAL_NAME']
        item_1['ALIAS'] = item['ALIAS']
        item_1['ADDRESS'] = item['ADDRESS']
        item_1['TEL'] = item['TEL']
        item_1['TYPE'] = item['TYPE']
        item_1['RATE'] = item['RATE']
        item_1['LINK'] = item['LINK']

        baidu_url = "https://api.map.baidu.com/?qt=gc&wd=%s&ie=utf-8&oue=1&fromproduct=jsapi&res=api&ak=BQhoozAa4tLcjRjiGqsFFA4X" % (item_1['ADDRESS'])
        yield scrapy.Request(baidu_url,  meta={ 'item_meta': item_1, 'flag': flag}, callback=self.parse_point)

    def parse_point(self, response):
        item = response.meta['item_meta']
        flag = response.meta['flag']
        # 解析json
        results = json.loads(response.body)
        try:
            point_lat = results['content']['coord']['x']
            point_lng = results['content']['coord']['y']
        except:
            point_lat = ""
            point_lng = ""

        item_1 = HospitalFamilyItem()
        item_1['POINT_LAT'] = str(point_lat)
        item_1['POINT_LNG'] = str(point_lng)
        item_1['NUM'] = item['NUM']
        print "_______________"+item['NUM']
        item_1['HOSPITAL_NAME'] = item['HOSPITAL_NAME']
        item_1['ADDRESS'] = item['ADDRESS']
        item_1['TEL'] = item['TEL']
        item_1['LINK'] = item['LINK']

        if flag == 1:
            item_1['IS_HOS'] = item['IS_HOS']
            item_1['NATURE'] = item['NATURE']
            item_1['ALIAS'] = item['ALIAS']
            item_1['TYPE'] = item['TYPE']
            item_1['RATE'] = item['RATE']
        else:
            item_1['IS_HOS'] = ""
            item_1['NATURE'] = ""
            item_1['ALIAS'] = ""
            item_1['TYPE'] = unicode("专科医院","utf-8")
            item_1['RATE'] = ""
        yield item_1