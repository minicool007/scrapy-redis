# -*- coding: utf-8 -*-
import re
import scrapy
from redis import Redis
from ..items import HospitalFamilyItem
from scrapy_redis.spiders import RedisSpider


# lpush hospital_spider:master_urls https://yyk.familydoctor.com.cn/area.html
class HospitalSpider(RedisSpider):
    name = 'hospital_master'
    redis_key = 'hospital_spider:master_urls'

    r = Redis(host="127.0.0.1", port=6379)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(HospitalSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        data_list = []
        # 抓取 省 城市 城区 医院名称 编号
        province = response.xpath("//dd/ul[@class='clearfix']/li")
        i = 0
        for pro in province:
            if i == 0:
                i = 1
                continue
            pro_url = pro.xpath('a/@href').extract()[0]
            pro_name = pro.xpath('a/text()').extract()[0]

            item = HospitalFamilyItem()
            item['PROVINCE'] = pro_name.strip()

            data = {'item_meta':item, 'url':pro_url}
            data_list.append(data)

        for data in data_list:
            print "---------------------------1"
            yield scrapy.Request(data['url'], meta={ 'item_meta': data['item_meta']}, callback=self.parse_city)

    def parse_city(self, response):
        item = response.meta['item_meta']
        data_list = []
        # 抓取 省 城市 城区 医院名称 编号
        province = response.xpath("//dd/ul[@class='clearfix']/li")
        i = 0
        for pro in province:
            if i == 0:
                i = 1
                continue
            city_url = pro.xpath('a/@href').extract()[0]
            city_name = pro.xpath('a/text()').extract()[0]

            item_1 = HospitalFamilyItem()
            item_1['CITY'] = city_name.strip()
            item_1['PROVINCE'] = item['PROVINCE']

            data = {'item_meta': item_1, 'url': city_url}
            data_list.append(data)

        for data in data_list:
            print "---------------------------2"
            yield scrapy.Request(data['url'], meta={'item_meta': data['item_meta']}, callback=self.parse_district)

    def parse_district(self, response):

        item = response.meta['item_meta']
        # item = response.meta['item_meta']
        # 需要判断是两层还是三层的
        block = response.xpath("//dd/ul[@class='clearfix']/li[1]/a/@href")
        if len(block) > 0:
            # 三层 lpush hospital_spider:master_urls https://yyk.familydoctor.com.cn/area_253_0_0_0_1.html
            flag = 1
        else:
            # 两层 lpush hospital_spider:master_urls https://yyk.familydoctor.com.cn/addarea_25_0_0_0_1.html
            flag = 2

        if flag == 1:
            data_list = []
            # 抓取 省 城市 城区 医院名称 编号
            district = response.xpath("//dd/ul[@class='clearfix']/li")
            i = 0
            for dis in district:
                if i == 0:
                    i = 1
                    continue
                dis_url = dis.xpath('a/@href').extract()[0]
                dis_name = dis.xpath('a/text()').extract()[0]

                item_1 = HospitalFamilyItem()
                item_1['DISTRICT'] = dis_name.strip()
                item_1['CITY'] = item['CITY']
                item_1['PROVINCE'] = item['PROVINCE']

                data = {'item_meta': item_1, 'url': dis_url}
                data_list.append(data)

            for data in data_list:
                print "---------------------------3"
                yield scrapy.Request(data['url'], meta = { "item_meta":data['item_meta']}, callback=self.parse_dis)

        elif flag == 2:
            url_total = []
            try:
                page_num = response.xpath("//*[@id='listContent']/div[23]/a[last()-1]/text()").extract()[0]
            except:
                page_num = 1
            numbers = re.findall(r'_(\d*)',response.url)
            if len(numbers) == 5:
                for i in range(0,int(page_num)+1):
                    url_tmp = "https://yyk.familydoctor.com.cn/addarea_%s_0_0_0_%s.html" % (numbers[0], i)
                    url_total.append(url_tmp)
            # 专科医院
            url_tmp = "https://yyk.familydoctor.com.cn/addarea_%s_0_0_1_%s.html" % (numbers[0], 1)
            url_total.append(url_tmp)
            for url in url_total:
                item_1 = HospitalFamilyItem()
                item_1['DISTRICT'] = item['CITY']
                item_1['CITY'] = item['PROVINCE']
                item_1['PROVINCE'] = item['PROVINCE']

                # self.r.lpush('hospital_spider:url_list', url)
                print "*********************************2"
                yield scrapy.Request(url, meta = {"item_meta":item_1}, callback=self.parse_page)
    def parse_page(self, response):
        item = response.meta['item_meta']
        # 判断是否为推荐页面
        tips = response.xpath("//*[@id='listContent']/div[@class='fd-no-record']")
        if len(tips) != 0:
            return
        hospital = response.xpath("//*[@id='listContent']/div/h3")
        if len(hospital) == 0:
            return
        print "抓取的" + response.url
        for hos in hospital:
            hos_url = hos.xpath("a/@href").extract()[0]
            hos_name = hos.xpath("a/text()").extract()[0]

            num = re.findall(r'(\d+)',hos_url)

            item_1 = HospitalFamilyItem()
            item_1['HOSPITAL_NAME'] = hos_name
            item_1['NUM'] = num[0]
            item_1['DISTRICT'] = item['DISTRICT']
            item_1['CITY'] = item['CITY']
            item_1['PROVINCE'] = item['PROVINCE']

            self.r.lpush('hospital_spider:slave1_urls', hos_url)
            yield item_1

    def parse_dis(self, response):
        item = response.meta['item_meta']
        url_total = []
        try:
            page_num = response.xpath("//*[@id='listContent']/div[23]/a[last()-1]/text()").extract()[0]
        except:
            page_num = 1
        numbers = re.findall(r'_(\d*)', response.url)
        if len(numbers) == 5:
            for i in range(0, int(page_num) + 1):
                url_tmp = "https://yyk.familydoctor.com.cn/addarea_%s_0_0_0_%s.html" % (numbers[0], i)
                url_total.append(url_tmp)
        # 专科医院
        url_tmp = "https://yyk.familydoctor.com.cn/addarea_%s_0_0_1_%s.html" % (numbers[0], 1)
        url_total.append(url_tmp)
        for url in url_total:
            # self.r.lpush('hospital_spider:url_list', url)
            print "*********************************3"
            yield scrapy.Request(url, meta={ "item_meta":item}, callback=self.parse_page)
