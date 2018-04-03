# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import SoufangNewItem
from scrapy_redis.spiders import RedisSpider


# lpush xzSoufang_spider:master_urls http://newhouse.xz.fang.com/house/s/
class XzsoufangSpider(RedisSpider):
    name = 'xzSoufang_master'
    redis_key = 'xzSoufang_spider:master_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(XzsoufangSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = []
        districts = response.xpath("//*[@id='quyu_name']/a")
        flag = 1
        for dis in districts:
            if flag == 1:
                flag = 2
                continue
            dis_name = dis.xpath("text()").extract()[0]
            dis_url = dis.xpath("@href").extract()[0]

            item = SoufangNewItem()
            item['DISTRICT'] = dis_name.encode("utf-8")
            item['CITY'] = "徐州"

            url = "http://newhouse.xz.fang.com"+dis_url
            data = {"url": url, "item": item}
            data_list.append(data)
        for data in data_list:
            item_list = []
            yield scrapy.Request(data['url'],meta={"item_meta":data['item'], "page":1, "item_list":item_list}, callback=self.parse_page)

    def parse_page(self, response):
        item = response.meta["item_meta"]
        page = response.meta["page"]
        item_list = response.meta["item_list"]

        solos = response.xpath("//div/div[1]/ul/li/div/div[2]/div[1]/div[1]/a[1]")
        for solo in solos:
            res_name = solo.xpath("text()").extract()[0]
            res_url = solo.xpath("@href").extract()[0].strip()

            num = re.findall(r'http://(.*?).fang.com',res_url)[0]

            item_1 = SoufangNewItem()
            item_1['RES_NAME'] = res_name.encode("utf-8").strip()
            item_1["NUM"] = str(num)
            item_1['DISTRICT'] = item['DISTRICT']
            item_1['CITY'] = item['CITY']

            item_list.append(item_1)
            self.r.lpush("xzSoufang_spider:slave_urls", res_url)

        # 下一页的按钮
        try:
            page_next = response.xpath("//*[@id='sjina_C01_47']/ul/li[2]/a[last()-1]/text()").extract()[0].encode("utf-8")
            if page_next == "下一页":
                flag = 1
            else:
                flag = 2
        except:
            flag = 2
        if flag == 1:
            page = page + 1
            next_url = response.xpath("///*[@id='sjina_C01_47']/ul/li[2]/a[last()-1]//@href").extract()[0]
            url = "http://newhouse.xz.fang.com"+next_url
            try:
                yield scrapy.Request(url, meta={"item_meta": item, "page":page, "item_list":item_list}, callback=self.parse_page)
            except:
                print ""
        else:
            print item['DISTRICT'] + "总页数：" + str(page)
            print "共有" + str(len(item_list)) + "个对象"
            for it in item_list:
                yield it



