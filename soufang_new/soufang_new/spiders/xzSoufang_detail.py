# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import SoufangNewItem
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# lpush xzSoufang_spider:slave8_urls http://yanlangongguanhedc.fang.com/?ctm=1.xz.xf_search.lplist.1
class InfoSpider(RedisSpider):
    name = 'xzSoufang_slave'
    redis_key = 'xzSoufang_spider:slave8_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        num = re.findall(r'http://(.*?).fang.com', response.url)[0]
        detail_url = response.xpath('/html/body/div[3]/div[3]/div[2]/div[1]/div[12]/div/p/a/@href').extract()[0].encode("utf-8")
        res_name = response.xpath("//div[@class='tit']/h1/strong/text()").extract()[0]
        if "http" not in detail_url:
            detail_url = "http://newhouse.xinyi.fang.com"+detail_url
        item = SoufangNewItem()
        item['LINK'] = detail_url
        item['RES_NAME'] = res_name.encode("utf-8")
        item['NUM'] = num

        baidu_url = response.xpath("//*[@id='iframe_map']/@src").extract()[0]
        yield scrapy.Request(baidu_url, meta={"item_meta":item}, callback=self.parse_point)

    def parse_point(self, response):
        item = response.meta['item_meta']
        # 解析楼盘id
        res_id = re.findall(r'newcode=(\d+)',response.url)[0]
        # 解析坐标点
        data = response.text.encode("utf-8")
        pattern1 = re.compile(r'"mapx":"([.\d]+)"')
        pattern2 = re.compile(r'"mapy":"([.\d]+)"')

        lng = pattern1.findall(data)[0]
        lat = pattern2.findall(data)[0]
        point = lng + "," + lat

        item_1 = SoufangNewItem()
        item_1["RES_NAME"] = item["RES_NAME"]
        item_1["RES_ID"] = res_id
        item_1["POINT"] = point
        item_1['NUM'] = item['NUM']
        item_1['LINK'] = item['LINK']

        yield scrapy.Request(item["LINK"],meta={"item_meta":item_1}, callback=self.parse_detail)
    def parse_detail(self, response):
        item = response.meta['item_meta']
        soup = BeautifulSoup(response.text, "lxml")
        list = soup.select("div.main-left > div")
        descript = list[0].select("p.intro")[0].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        list_1 = list[0].select(" ul > li")
        # 基本信息
        manage_type = list_1[0].select("div.list-right")[0].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        manage_desc = list_1[-2].select("div.list-right-floor")[0].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        state = list_1[-1].select("div.list-right-floor")[0].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')

        item_1 = list_1[1].select("div.list-right")
        build_type = item_1[1].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        used_year = item_1[3].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        location = item_1[4].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        sale_state = item_1[5].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        open_time = item_1[7].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','').replace('[开盘时间详情]','')
        success_time = item_1[8].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        sale_address = item_1[9].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        area = item_1[11].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        build_area = item_1[12].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        volum = item_1[13].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        green = item_1[14].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        park = item_1[15].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        build_num = item_1[16].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        house_num = item_1[17].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        manage_company = item_1[18].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')
        manage_fee = item_1[19].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')

        item_2 = list_1[1].select("div.list-right-text")
        developer = item_2[0].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','').replace('[房企申请入驻]','')
        address = item_2[1].get_text().encode("utf-8").replace("\t","").replace("\n","").replace(' ','')

        item1_1 = SoufangNewItem()
        item1_1["RES_NAME"] = item['RES_NAME']
        item1_1["NUM"] = item['NUM']
        item1_1["RES_ID"] = item["RES_ID"]
        item1_1["POINT"] = item["POINT"]
        item1_1["ADDRESS"] = address
        item1_1["MANAGE_TYPE"] = manage_type
        item1_1["BUILD_TYPE"] = build_type
        item1_1["USED_YEAR"] = used_year
        item1_1["LOCATION"] = location
        item1_1["DEVELOPER"] = developer
        item1_1["OPEN_TIME"] = open_time
        item1_1["SUCCESS_TIME"] = success_time
        item1_1["SALE_STATE"] = sale_state
        item1_1["SALE_ADDRESS"] = sale_address
        item1_1["MANAGE_COMPANY"] = manage_company
        item1_1["MANAGE_FEE"] = manage_fee
        item1_1["MANAGE_DESC"] = manage_desc
        item1_1["BUILD_AREA"] = build_area
        item1_1["AREA"] = area
        item1_1["GREEN"] = green
        item1_1["VOLUM"] = volum
        item1_1["PARK"] = park
        item1_1["BUILD_NUM"] = build_num
        item1_1["HOUSE_NUM"] = house_num
        item1_1["STATE"] = state
        item1_1["DESCRIPT"] = descript
        item1_1["LINK"] = item['LINK']

        yield item1_1