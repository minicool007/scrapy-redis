# -*- coding: utf-8 -*-
import redis

import MySQLdb

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

db = MySQLdb.connect("localhost","root","123456","dbtest" )
cursor = db.cursor()

try:
    # 到数据库查询 漏抓的num，并放入redis数据库
    sql = "SELECT hos_family.NUM FROM hos_family \
            LEFT JOIN hos_detail \
            ON hos_detail.NUM = hos_family.NUM AND hos_detail.HOSPITAL_NAME = hos_family.HOSPITAL_NAME \
            WHERE hos_detail.NUM is NULL"
    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results)
    for row in results:
        num = row[0]
        url = "https://yyk.familydoctor.com.cn/%s/" % num
        r.rpush("hospital_spider:slave8_urls",url)
except:
    print "error"

db.close()
