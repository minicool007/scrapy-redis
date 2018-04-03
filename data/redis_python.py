# -*- coding: utf-8 -*-
import redis
import json

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 读取redis数据库的内容，并写入json

# dict = {'xzRecycle_spider:slave_urls':r.lrange('xzRecycle_spider:slave_urls',0,-1)}
# with open("D:/PROJ/python/scrapy_redis/data/data_xzRecycle.json","w") as dump_f:
#     json.dump(dict,dump_f)

# 读取json并写入redis

with open("D:/PROJ/python/scrapy_redis/data/data_xzAnjuke.json",'r') as load_f:
    load_dict = json.load(load_f)
    value = load_dict['xzAnjuke_spider:slave_urls']
    for m in value:
        r.rpush("xzAnjuke_spider:slave8_urls", m)



