# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from redis import Redis

class Slave1Spider(RedisSpider):

    name = 'slave1'
    redis_key = 'hospital_spider:slave1_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(Slave1Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        r = Redis(host="10.30.128.247", port=6380)
        pass