# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import AnjukeXiaoquItem
from scrapy_redis.spiders import RedisSpider
# lpush xzRecycle_spider:master_urls https://fz.anjuke.com/community/
class XzrecycleSpider(RedisSpider):
    name = 'xzRecycle_master'
    redis_key = 'xzRecycle_spider:master_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(XzrecycleSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = []
        districts = response.xpath("//div[1]/span[2]/a")
        flag = 1
        for dis in districts:
            if flag == 1:
                flag = 2
                continue
            dis_url = dis.xpath("@href").extract()[0]
            dis_name = dis.xpath("text()").extract()[0]

            item = AnjukeXiaoquItem()
            item['DISTRICT'] = dis_name.encode("utf-8")
            item['CITY'] = "徐州"

            data = {"url": dis_url, "item": item}
            data_list.append(data)
        for data in data_list:
            item_list = []
            yield scrapy.Request(data['url'],meta={"item_meta":data['item'], "page":1, "item_list":item_list}, callback=self.parse_page)

    def parse_page(self, response):
        item = response.meta["item_meta"]
        page = response.meta["page"]
        item_list = response.meta["item_list"]

        # 解析列表内容
        solos = response.xpath("//*[@id='list-content']/div[@class='li-itemmod']/a")
        for solo in solos:
            res_name = solo.xpath("@title").extract()[0].strip()
            res_url = solo.xpath("@href").extract()[0]
            num = re.findall(r'(\d+)', res_url)[0]

            item_1 = AnjukeXiaoquItem()
            item_1['RES_NAME'] = res_name.encode("utf-8")
            item_1["NUM"] = str(num)
            item_1['DISTRICT'] = item['DISTRICT']
            item_1['CITY'] = item['CITY']

            item_list.append(item_1)
            self.r.lpush("xzRecycle_spider:slave_urls", res_url)
        # 下一页的按钮
        try:
            page_next = response.xpath("//div[@class='page-content']/div/a[last()]/text()").extract()[0].encode("utf-8")
            if page_next == '下一页 >':
                flag = 1
            else:
                flag = 2
        except:
            flag = 2
        if flag == 1:
            page = page + 1
            next_url = response.xpath("//div[@class='page-content']/div/a[last()]/@href").extract()[0]
            yield scrapy.Request(next_url, meta={"item_meta": item, "page":page, "item_list":item_list}, callback=self.parse_page)
        else:
            print item['DISTRICT'] + "总页数：" + str(page)
            print "共有" + str(len(item_list)) + "个对象"
            for it in item_list:
                yield it

