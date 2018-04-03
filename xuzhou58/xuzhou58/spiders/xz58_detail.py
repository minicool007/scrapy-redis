# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import Xuzhou58Item
from scrapy_redis.spiders import RedisSpider
import re
from bs4 import BeautifulSoup
# lpush xz58_spider:slave8_urls http://xz.58.com/xiaoqu/lvdishijicheng/?iuType=p_&PGTID=0d011138-001d-7c92-e083-4453d3523747&ClickID=2
class InfoSpider(RedisSpider):
    name = 'xz58_slave'
    redis_key = 'xz58_spider:slave8_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = response.text.encode("utf-8")
        pattern1 = re.compile(r'infoid: "(.*?)"')
        pattern2 = re.compile(r'lat: "(.*?)"')
        pattern3 = re.compile(r'lon: "(.*?)"')

        id = pattern1.findall(data)[0]
        lat = pattern2.findall(data)[0]
        lon = pattern3.findall(data)[0]

        list_1 = str(response.url).split("/")
        num = list_1[4] + list_1[5]
        left_item = response.xpath("//table[@class='info-tb']/tr/td[2]")
        district = left_item[0].xpath("@title").extract()[0] # 商圈区域
        build_type = left_item[1].xpath("@title").extract()[0]
        type = left_item[2].xpath("@title").extract()[0] # 产权类别
        used_time = left_item[3].xpath("@title").extract()[0] # 产权年限
        build_time = left_item[4].xpath("@title").extract()[0] # 建筑年代
        area = left_item[5].xpath("@title").extract()[0]  # 占地面积
        park = left_item[6].xpath("@title").extract()[0]  # 停车位
        manage_company = left_item[7].xpath("@title").extract()[0]  # 物业公司
        developer = left_item[8].xpath("@title").extract()[0]  # 开发商
        house_num = left_item[9].xpath("string(.)").extract()[0]  # z在售房源

        right_item = response.xpath("//table[@class='info-tb']/tr/td[4]")
        address = right_item[0].xpath("@title").extract()[0]  # 详细地址
        manage_fee = right_item[2].xpath("@title").extract()[0] # 物业费
        volum = right_item[3].xpath("@title").extract()[0]  # 容积率
        green = right_item[4].xpath("@title").extract()[0]  # 绿化率
        build_area = right_item[5].xpath("@title").extract()[0]  # 建筑面积
        rent_num = right_item[6].xpath("string(.)").extract()[0]  # 在租房源
        try:
            description = response.xpath("//div[@class='detail-mod desc-mod']/p/text()").extract()[0].encode('utf-8').strip()
        except:
            description = ""

        item = Xuzhou58Item()
        item['NUM'] = num
        item['POINT'] = lon + "," + lat
        item['ADDRESS'] = address.encode('utf-8')
        item['USED_TIME'] = used_time.encode('utf-8')
        item['TYPE'] = type.encode('utf-8')
        item['BUILD_TIME'] = build_time.encode('utf-8')
        item['BUILD_TYPE'] = build_type.encode('utf-8')
        item['MANAGE_COMPANY'] = manage_company.encode('utf-8')
        item['MANAGE_FEE'] = manage_fee.encode('utf-8')
        item['DEVELOPER'] = developer.encode('utf-8')
        item['BUILD_AREA'] = build_area.encode('utf-8')
        item['AREA'] = area.encode('utf-8')
        item['GREEN'] = green.encode('utf-8')
        item['VOLUM'] = volum.encode('utf-8')
        item['PARK'] = park.encode('utf-8')
        item['DESCRIPTION'] = description.replace('\r','').replace('\t','').replace(' ','').replace('\n','')
        item['HOUSE_NUM'] = house_num.encode('utf-8').replace('\r','').replace('\t','').replace(' ','').replace('\n','')
        item['RENT_NUM'] = rent_num.encode('utf-8').replace('\r','').replace('\t','').replace(' ','').replace('\n','')
        item['LINK'] = response.url
        item['COM_ID'] = id

        yield item
