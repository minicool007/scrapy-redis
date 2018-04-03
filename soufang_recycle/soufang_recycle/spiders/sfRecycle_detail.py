# -*- coding: utf-8 -*-
import scrapy
import re
from redis import Redis
from ..items import SoufangRecycleItem
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
# lpush sfRecycle_spider:slave8_urls  http://yuyuan0516.fang.com/2/esf/
class InfoSpider(RedisSpider):
    name = 'sfRecycle_slave'
    redis_key = 'sfRecycle_spider:slave8_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        num1 = re.findall(r'/([a-z0-9]+)', response.url)
        num = ""
        for n in num1:
            num = num + n + "_"
        num = num[0:-1]
        if "esf" in num:
            detail_url = response.url.replace("/esf/","/") + "xiangqing/"
        else:
            detail_url = response.url + "xiangqing/"


        try:
            res_name = response.xpath("//div[@class='firstright']/div[1]/h1/strong/text()").extract()[0]
            house_num = response.xpath("//*[@id='xqwxqy_C01_16']/a[1]/div/p[2]/text()").extract()[0]
            rent_num = response.xpath("//*[@id='xqwxqy_C01_16']/a[3]/div/p[2]/text()").extract()[0]
        except:
            res_name = response.xpath("//div[1]/div[1]/div/h1/strong/text()").extract()[0]
            house_num = ""
            rent_num = ""
        try:
            school = response.xpath("//*[@id='body']/div[6]/div[2]/div[3]/ul/li[7]/a/text()").extract()[0]
        except:
            school = ""

        item = SoufangRecycleItem()
        item['LINK'] = detail_url
        item['RES_NAME'] = res_name.encode("utf-8")
        item['NUM'] = num
        item['HOUSE_NUM'] = house_num.encode("utf-8")
        item['RENT_NUM'] = rent_num.encode("utf-8")

        item['SCHOOL'] = school

        baidu_url = response.xpath("//*[@id='iframe_map']/@src").extract()[0]
        yield scrapy.Request(baidu_url, meta={"item_meta": item}, callback=self.parse_point)
    def parse_point(self, response):
        item = response.meta['item_meta']
        # 解析坐标点
        data = response.text.encode("utf-8")
        pattern1 = re.compile(r'"baidu_coord_x":"([.\d]+)"')
        pattern2 = re.compile(r'"baidu_coord_y":"([.\d]+)"')
        pattern3 = re.compile(r'"newCode":"(\d+)"')

        lng = pattern1.findall(data)[0]
        lat = pattern2.findall(data)[0]
        res_id =  pattern3.findall(data)[0]
        point = lng + "," + lat

        item_1 = SoufangRecycleItem()
        item_1["RES_NAME"] = item["RES_NAME"]
        item_1["RES_ID"] = res_id
        item_1["POINT"] = point
        item_1['NUM'] = item['NUM']
        item_1['LINK'] = item['LINK']
        item_1['HOUSE_NUM'] = item['HOUSE_NUM']
        item_1['RENT_NUM'] = item['RENT_NUM']
        item_1['SCHOOL'] = item['SCHOOL']

        yield scrapy.Request(item["LINK"],meta={"item_meta":item_1}, callback=self.parse_detail)
    def parse_detail(self, response):
        item = response.meta['item_meta']
        # 基本信息
        dict_basic = {}
        basic = response.xpath("//div[@class='con_left']/div[2]/div[2]/dl/dd")
        for i in range(0, len(basic)):
            key = basic[i].xpath("strong/text()").extract()[0].encode('utf-8').replace('：', '').replace(' ', '')
            try:
                value = basic[i].xpath('@title').extract()[0].encode('utf-8').replace('\r', '').replace('\t', '').replace(' ', '').replace('\n', '')
            except:
                try:
                    value = basic[i].xpath('text()').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
                except:
                    value = basic[i].xpath('span/@title').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace( ' ', '').replace('\n', '')
            dict_basic[key] = value

        address = dict_basic['小区地址'].strip()
        if dict_basic.has_key("所属区域"):
            district = dict_basic['所属区域'].strip()
        else:
            district = ''
        if dict_basic.has_key("环线位置"):
            location = dict_basic['环线位置'].strip().replace("：","")
        else:
            location = ''
        if dict_basic.has_key("产权描述"):
            discript = dict_basic['产权描述'].strip()
        else:
            discript = ''
        if dict_basic.has_key("物业类别"):
            manage_type = dict_basic['物业类别'].strip()
        else:
            manage_type = ''
        if dict_basic.has_key("建筑年代"):
            build_year = dict_basic['建筑年代'].strip()
        else:
            build_year = ''
        if dict_basic.has_key("开发商"):
            developer = dict_basic['开发商'].strip()
        else:
            developer = ''
        if dict_basic.has_key("建筑类型"):
            build_type = dict_basic['建筑类型'].strip()
        else:
            build_type = ''
        if dict_basic.has_key("建筑面积"):
            build_area = dict_basic['建筑面积'].strip()
        else:
            build_area = ''
        if dict_basic.has_key("占地面积"):
            area = dict_basic['占地面积'].strip()
        else:
            area = ''
        if dict_basic.has_key("物业公司"):
            manage_company = dict_basic['物业公司'].strip()
        else:
            manage_company = ''
        if dict_basic.has_key("绿化率"):
            green = dict_basic['绿化率'].strip()
        else:
            green = ''
        if dict_basic.has_key("容积率"):
            volum = dict_basic['容积率'].strip()
        else:
            volum = ''
        if dict_basic.has_key("物业费"):
            manage_fee = dict_basic['物业费'].strip()
        else:
            manage_fee = ''
        if dict_basic.has_key("附加信息"):
            info = dict_basic['附加信息'].strip()
        else:
            info = ''
        if dict_basic.has_key("物业办公地点"):
            manage_location = dict_basic['物业办公地点'].strip()
        else:
            manage_location = ''
        if dict_basic.has_key("物业办公电话"):
            manage_tel = dict_basic['物业办公电话'].strip()
        else:
            manage_tel = ''
        if dict_basic.has_key("建筑结构"):
            build_structure = dict_basic['建筑结构'].strip()
        else:
            build_structure = ''
        # 配套设施
        dict_suit = {}
        suit_keys = response.xpath("//div[@class='con_left']/div[3]/div[2]/dl/dt/strong/text()").extract()
        suit_values = response.xpath("//div[@class='con_left']/div[3]/div[2]/dl/dt")
        for i in range(0, len(suit_keys)):
            key = suit_keys[i].encode('utf-8').replace('：', '').replace(' ', '')
            try:
                value = suit_values[i].xpath('@title').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
            except:
                try:
                    value = suit_values[i].xpath('text()').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
                except:
                    value = suit_values[i].xpath('span/@title').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
            dict_suit[key] = value
        if dict_suit.has_key("停车位"):
            park = dict_suit['停车位'].strip()
        else:
            park = ''
        # 历史开盘信息
        dict_res = {}
        res_keys = response.xpath("//div[@class='con_left']/div[7]/div[2]/dl/dd/strong/text()").extract()
        res_values = response.xpath("//div[@class='con_left']/div[7]/div[2]/dl/dd")
        for i in range(0, len(res_keys)):
            key = res_keys[i].encode('utf-8').replace('：', '').replace(' ', '')
            try:
                value = res_values[i].xpath('@title').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
            except:
                try:
                    value = res_values[i].xpath('text()').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
                except:
                    value = res_values[i].xpath('span/@title').extract()[0].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
            dict_res[key] = value
        if dict_res.has_key("开盘时间"):
            open_time = dict_res['开盘时间'].strip()
        else:
            open_time = ''
        if dict_res.has_key("交房时间"):
            success_time = dict_res['交房时间'].strip()
        else:
            success_time = ''

        item_1 = SoufangRecycleItem()
        item_1['NUM'] = item['NUM']
        item_1['RES_ID'] = item['RES_ID']
        item_1['RES_NAME'] = item['RES_NAME']
        item_1['POINT'] = item['POINT']
        item_1['ADDRESS'] = address
        item_1['LOCATION'] = location
        item_1['BUILD_YEAR'] = build_year
        item_1['MANAGE_TYPE'] = manage_type
        item_1['DESCRIPTION'] = discript
        item_1['BUILD_STRUCTURE'] = build_structure
        item_1['BUILD_TYPE'] = build_type
        item_1['MANAGE_COMPANY'] = manage_company
        item_1['MANAGE_LOCATION'] = manage_location
        item_1['MANAGE_TEL'] = manage_tel
        item_1['MANAGE_FEE'] = manage_fee
        item_1['INFO'] = info
        item_1['BUILD_AREA'] = build_area
        item_1['AREA'] = area
        item_1['GREEN'] = green
        item_1['VOLUM'] = volum
        item_1['DEVELOPER'] = developer
        item_1['OPEN_TIME'] = open_time
        item_1['SUCCESS_TIME'] = success_time
        item_1['PARK'] = park
        item_1['SCHOOL'] = item["SCHOOL"]
        item_1['HOUSE_NUM'] = item['HOUSE_NUM']
        item_1['RENT_NUM'] = item['RENT_NUM']
        item_1['LINK'] = item['LINK']

        yield item_1
