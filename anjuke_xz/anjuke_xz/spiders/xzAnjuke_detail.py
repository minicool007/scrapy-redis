# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import AnjukeXzItem
from scrapy_redis.spiders import RedisSpider
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class InfoSpider(RedisSpider):
    name = 'xzAnjuke_slave'
    redis_key = 'xzAnjuke_spider:slave8_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(InfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data = response.text.encode("utf-8")
        pattern1 = re.compile(r'Loupan.Map(.*?);')
        try:
            s = pattern1.search(data).group(0)
            res = re.findall(r'([.\d]+)', s)
            point = res[2] + "," + res[1]
        except:
            point = "暂无数据"

        num = re.findall(r'(\d+).html', response.url)[0]

        item = AnjukeXzItem()
        item["NUM"] = num
        item["RES_ID"] = num
        item["POINT"] = point
        item["LINK"] = response.url

        url = "https://xz.fang.anjuke.com/loupan/canshu-%s.html" % num
        yield scrapy.Request(url, meta={"item_meta":item}, callback=self.parse_canshu)

    def parse_canshu(self, response):
        item = response.meta["item_meta"]

        # 基本信息
        dict_basic = {}
        basic_keys = response.xpath("//*[@id='container']/div[1]/div[1]/div[1]/div[2]/ul/li/div[1]/text()").extract()
        basic_values = response.xpath("//*[@id='container']/div[1]/div[1]/div[1]/div[2]/ul/li/div[2]")
        for i in range(0, len(basic_keys)):
            key = basic_keys[i]
            value = basic_values.xpath('string(.)').extract()[i].encode('utf-8').replace('\r','').replace('\t','').replace(' ','').replace('\n','')
            dict_basic[key] = value
        res_name = dict_basic['楼盘名称'.decode('utf-8')].strip()
        if dict_basic.has_key("物业类型".decode('utf-8')):
            manage_type = dict_basic['物业类型'.decode('utf-8')].strip()
        else:
            manage_type = ''
        if dict_basic.has_key("开发商".decode('utf-8')):
            developer = dict_basic['开发商'.decode('utf-8')].strip()
        else:
            developer = ''
        if dict_basic.has_key("区域位置".decode('utf-8')):
            district = dict_basic['区域位置'.decode('utf-8')].strip()
        else:
            district = ''
        if dict_basic.has_key("楼盘地址".decode('utf-8')):
            address = dict_basic['楼盘地址'.decode('utf-8')].strip()
        else:
            address = ''
        # 销售信息
        dict_sale = {}
        sale_keys = response.xpath("//*[@id='container']/div[1]/div[1]/div[2]/div[2]/ul/li/div[1]/text()").extract()
        sale_values = response.xpath("//*[@id='container']/div[1]/div[1]/div[2]/div[2]/ul/li/div[2]")
        for i in range(0, len(sale_keys)):
            key = sale_keys[i]
            try:
                value = sale_values.xpath('string(.)').extract()[i].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
            except:
                print ""
            dict_sale[key] = value
        if dict_sale.has_key("最新开盘".decode('utf-8')):
            new_sale = dict_sale['最新开盘'.decode('utf-8')].strip()
        else:
            new_sale = ''
        if dict_sale.has_key("交房时间".decode('utf-8')):
            success_time = dict_sale['交房时间'.decode('utf-8')].strip()
        else:
            success_time = ''
        # 小区情况
        dict_state = {}
        state_keys = response.xpath("//*[@id='container']/div[1]/div[1]/div[3]/div[2]/ul/li/div[1]/text()").extract()
        state_values = response.xpath("//*[@id='container']/div[1]/div[1]/div[3]/div[2]/ul/li/div[2]")
        for i in range(0, len(state_keys)):
            key = state_keys[i]
            try:
                value = state_values.xpath('string(.)').extract()[i].encode('utf-8').replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
            except:
                print ""

            dict_state[key] = value
        if dict_state.has_key("建筑类型".decode('utf-8')):
            build_type = dict_state["建筑类型".decode('utf-8')].strip()
        else:
            build_type = ''
        if dict_state.has_key("产权年限".decode('utf-8')):
            used_time = dict_state["产权年限".decode('utf-8')].strip()
        else:
            used_time = ''
        if dict_state.has_key("楼层状况".decode('utf-8')):
            state = dict_state["楼层状况".decode('utf-8')].strip()
        else:
            state = ''
        if dict_state.has_key("容积率".decode('utf-8')):
            volum = dict_state["容积率".decode('utf-8')].strip()
        else:
            volum = ''
        if dict_state.has_key("绿化率".decode('utf-8')):
            green = dict_state["绿化率".decode('utf-8')].strip()
        else:
            green = ''
        if dict_state.has_key("规划户数".decode('utf-8')):
            plan_num = dict_state["规划户数".decode('utf-8')].strip()
        else:
            plan_num = ''
        if dict_state.has_key("工程进度".decode('utf-8')):
            proceed = dict_state["工程进度".decode('utf-8')].strip()
        else:
            proceed = ''
        if dict_state.has_key("物业管理费".decode('utf-8')):
            manage_fee = dict_state["物业管理费".decode('utf-8')].strip()
        else:
            manage_fee = ''
        if dict_state.has_key("物业公司".decode('utf-8')):
            manage_company = dict_state["物业公司".decode('utf-8')].strip()
        else:
            manage_company = ''
        if dict_state.has_key("车位数".decode('utf-8')):
            park_num = dict_state["车位数".decode('utf-8')].strip()
        else:
            park_num = ''
        if dict_state.has_key("车位比".decode('utf-8')):
            park_rate = dict_state["车位比".decode('utf-8')].strip()
        else:
            park_rate = ''

        item_1 = AnjukeXzItem()
        item_1['RES_NAME'] = res_name
        item_1['DISTRICT'] = district
        item_1['NUM'] = item['NUM']
        item_1['RES_ID'] = item['RES_ID']
        item_1['POINT'] = item['POINT']
        item_1["ADRESS"] = address.replace('[查看地图]','')
        item_1["MANAGE_COMPANY"] = manage_company
        item_1["MANAGE_FEE"] = manage_fee
        item_1["BUILD_AREA"] = ""
        item_1["GREEN"] = green.replace('[查看详情]','')
        item_1["VOLUM"] = volum.replace('[查看详情]','')
        item_1["DEVELOPER"] = developer
        item_1["NEW_SALE"] = new_sale
        item_1["SUCCESS_TIME"] = success_time
        item_1["PARK_NUM"] = park_num
        item_1["PARK_RATE"] = park_rate.replace('[查看详情]','')
        item_1["USED_TIME"] = used_time.replace('[查看详情]','')
        item_1["MANAGE_TYPE"] = manage_type
        item_1["BUILD_TYPE"] = build_type.replace('[查看详情]','')
        item_1["PLAN_NUM"] = plan_num.replace('[查看详情]','')
        item_1["STATE"] = state.replace('\r', '').replace('\t','').replace(' ', '').replace('\n', '')
        item_1["PROCCEED"] = proceed
        item_1["LINK"] = item["LINK"]

        yield item_1


