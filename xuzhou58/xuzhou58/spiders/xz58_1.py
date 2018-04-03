# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import Xuzhou58Item
from scrapy_redis.spiders import RedisSpider

# lpush xz58_spider_1:master_urls http://xz.58.com/xiaoqu/

class Xz58Spider(RedisSpider):
    name = 'xz58_master_1'
    redis_key = 'xz58_spider_1:master_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Xz58Spider, self).__init__(*args, **kwargs)

    def parse(self, response):

        item = Xuzhou58Item()
        item["DISTRICT"] = "睢宁"
        item["CITY"] = "徐州市"
        url = "http://zz.58.com/xiaoqu/11350/"
        item_list = []
        aa = True
        yield scrapy.Request(url, meta = {"item_meta":item, "page": 1, "item_list":item_list, "aa":aa}, callback = self.parse_page)

    # 通过点击下一页 实现翻页
    def parse_page(self, response):
        item = response.meta["item_meta"]
        page = response.meta["page"]
        item_list = response.meta["item_list"]
        aa = response.meta["aa"]
        # 解析列表页面
        unique_list = response.xpath("//table/tbody/tr/td[2]/ul/li[1]/a")

        for unique in unique_list:
            url = unique.xpath("@href").extract()[0]
            name = unique.xpath("text()").extract()[0].strip()
            try:
                alias = unique.xpath("span/text()").extract()[0]
            except:
                alias = ""
            # 提取字符串作为唯一标识
            list_1 = url.split("/")
            num = list_1[4]

            item_1 = Xuzhou58Item()
            item_1["COMUNITY_NAME"] = name.encode("utf-8")
            try:
                item_1["ALIAS"] = alias.encode("utf-8").replace('(','').replace(')','')
            except:
                item_1["ALIAS"] = alias.encode("utf-8")
            item_1["NUM"] = num.encode("utf-8")
            item_1["DISTRICT"] = item["DISTRICT"]
            item_1["CITY"] = item["CITY"]
            item_list.append(item_1)

            self.r.lpush("xz58_spider:slave_urls",url)

        # 下一页的按钮 由于最后两个页不能漏掉
        if aa:
            try:
                page_next = response.xpath("//*[@id='xiaoquPager']/a[last()]/span/text()").extract()[0].encode("utf-8")
                if page_next == "下一页":
                    flag = 1
                else:
                    flag = 1
                    aa = False
            except:
                flag = 2
        else:
            flag = 2
        if flag == 1:
            page = page + 1
            next_url = response.xpath("//*[@id='xiaoquPager']/a[last()]/@href").extract()[0]
            yield scrapy.Request(next_url, meta={"item_meta": item, "page": page, "item_list": item_list, "aa":aa},
                                 callback=self.parse_page)
        else:
            print item['DISTRICT'] + "总页数：" + str(page)
            print "共有" + str(len(item_list)) + "个对象"
            for it in item_list:
                yield it


