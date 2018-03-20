# -*- coding: utf-8 -*-
import redis
import json

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# 读取redis数据库的内容，并写入json

# dict = {'hospital_spider:slave1_urls':r.lrange('hospital_spider:slave1_urls',0,-1)}
# with open("./data/data1.json","w") as dump_f:
#     json.dump(dict,dump_f)

# 读取json并写入redis

with open("./data/data1.json",'r') as load_f:
    load_dict = json.load(load_f)
    value = load_dict['hospital_spider:slave1_urls']
    for m in value:
        r.rpush("hospital_spider:slave8_urls", m)



