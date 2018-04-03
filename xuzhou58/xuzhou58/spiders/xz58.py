# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import Xuzhou58Item
from scrapy_redis.spiders import RedisSpider

# lpush xz58_spider:master_urls http://xz.58.com/xiaoqu/

class Xz58Spider(RedisSpider):
    name = 'xz58_master'
    redis_key = 'xz58_spider:master_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Xz58Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = []
        districts = response.xpath("//div[@class='relative']/dl[1]/dd/a")
        flag = 1
        for dis in districts:
            if flag == 1:
                flag = 2
                continue
            # 小区名称
            dis_name = dis.xpath("text()").extract()[0]
            # 小区url
            dis_num = dis.xpath("@listname").extract()[0]
            dis_url = "http://xz.58.com/xiaoqu/%s/" % dis_num
            item = Xuzhou58Item()
            item["DISTRICT"] = dis_name.encode("utf-8")
            item["CITY"] = "徐州市"

            data = {"item": item, "url": dis_url}
            data_list.append(data)
        for data in data_list:
            item_list = []
            aa = True
            yield scrapy.Request(data["url"], meta = {"item_meta":data["item"], "page": 1, "item_list":item_list, "aa":aa}, callback = self.parse_page)

    # 通过点击下一页 实现翻页
    def parse_page(self, response):
        item = response.meta["item_meta"]
        page = response.meta["page"]
        item_list = response.meta["item_list"]
        aa = response.meta["aa"]
        # 解析列表页面
        unique_list = response.xpath("//table/tbody/tr/td[2]/ul")

        for unique in unique_list:
            url = unique.xpath("li[1]/a/@href").extract()[0]
            name = unique.xpath("li[1]/a/text()").extract()[0].strip()
            try:
                alias = unique.xpath("li[1]/a/span/text()").extract()[0]
            except:
                alias = ""
            dis = unique.xpath("li[2]/text()").extract()[0].encode('utf-8')
            if item['DISTRICT'] in dis:

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


