# -*- coding: utf-8 -*-
import redis

import MySQLdb

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

db = MySQLdb.connect("localhost","root","123456","dbtest" )
cursor = db.cursor()

try:
    # 到数据库查询 漏抓的num，并放入redis数据库
    sql = "SELECT sfrecycle.NUM,sfrecycle.LINK FROM sfrecycle \
         LEFT JOIN sfrecycle_detail \
         ON sfrecycle.NUM = sfrecycle_detail.NUM \
         WHERE sfrecycle_detail.NUM is NULL"
    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results)
    for row in results:
        num = row[0]
        if num.isdigit():
            continue
        url = row[1]
        r.rpush("sfRecycle_spider:slave8_urls",url)
except:
    print "error"

db.close()
