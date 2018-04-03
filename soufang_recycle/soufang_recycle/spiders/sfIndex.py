# -*- coding: utf-8 -*-
import scrapy
import re
import scrapy
from redis import Redis
from ..items import SoufangRecycleItem
from scrapy_redis.spiders import RedisSpider

# lpush sfRecycle:master_urls http://esf.xz.fang.com/housing/
class SfrecycleSpider(RedisSpider):
    name = 'sfRecycle_index'
    redis_key = 'sfRecycle:index_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(SfrecycleSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = []
        dis = response.xpath("//*[@id='houselist_B03_02']/div[1]/a")
        dis_name = dis[0].xpath("text()").extract()[0]
        dis_url = dis[0].xpath("@href").extract()[0]

        item = SoufangRecycleItem()
        item['DISTRICT'] = dis_name.encode("utf-8")
        item['CITY'] = "徐州"

        url = "http://esf.xz.fang.com" + dis_url

        item_list = []
        yield scrapy.Request(url, meta={"item_meta": item, "page": 1, "item_list": item_list},
                             callback=self.parse_page)
    def parse_page(self, response):
        item = response.meta["item_meta"]
        page = response.meta["page"]
        item_list = response.meta["item_list"]

        solos = response.xpath("//div[@class='houseList']/div/dl/dd")
        for solo in solos:
            res_name = solo.xpath("p[1]/a/text()").extract()[0]
            res_url = solo.xpath("p[1]/a/@href").extract()[0].strip()
            build_year = solo.xpath("ul/li[3]/text()").extract()[0].strip()
            if "http" in res_url:
                num1 = re.findall(r'/([a-z0-9]+)', res_url)
                num = ""
                for n in num1:
                    num = num + n + "_"
                num = num[0:-1]

                link = res_url
                item_1 = SoufangRecycleItem()
                item_1['RES_NAME'] = res_name.encode("utf-8").strip()
                item_1["NUM"] = str(num)
                item_1['DISTRICT'] = item['DISTRICT']
                item_1['CITY'] = item['CITY']
                item_1["BUILD_YEAR"] = build_year
                item_1["LINK"] = link

                item_list.append(item_1)
                self.r.lpush("sfRecycle_spider:slave_urls", res_url)
            else:
                link = "http://esf.xz.fang.com"+res_url
                res_id = re.findall(r'house-xm(\d+)',res_url)[0]
                item_1 = SoufangRecycleItem()
                item_1['RES_NAME'] = res_name.encode("utf-8").strip()
                item_1["NUM"] = res_id
                item_1['DISTRICT'] = item['DISTRICT']
                item_1['CITY'] = item['CITY']
                item_1["BUILD_YEAR"] = build_year
                item_1["LINK"] = link
                item_list.append(item_1)
                continue
        # 下一页的按钮
        try:
            page_next = response.xpath("//*[@id='PageControl1_hlk_next']/text()").extract()[0].encode("utf-8")
            if page_next == "下一页":
                flag = 1
            else:
                flag = 2
        except:
            flag = 2
        if flag == 1:
            page = page + 1
            next_url = response.xpath("//*[@id='PageControl1_hlk_next']/@href").extract()[0]
            url = "http://esf.xz.fang.com"+next_url
            yield scrapy.Request(url, meta={"item_meta": item, "page":page, "item_list":item_list}, callback=self.parse_page)
        else:
            print item['DISTRICT'] + "总页数：" + str(page)
            print "共有" + str(len(item_list)) + "个对象"
            if len(item_list) != 0:
                for it in item_list:
                    yield it