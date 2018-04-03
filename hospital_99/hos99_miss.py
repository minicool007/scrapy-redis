# -*- coding: utf-8 -*-
import redis
import re
import MySQLdb

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

db = MySQLdb.connect("localhost","root","123456","dbtest" )
cursor = db.cursor()

try:
    # 到数据库查询 漏抓的num，并放入redis数据库
    sql = "SELECT hos99.NUM FROM hos99 " \
          "LEFT JOIN hos99_detail ON hos99.NUM = hos99_detail.NUM " \
          "WHERE hos99_detail.NUM is NULL"
    cursor.execute(sql)
    results = cursor.fetchall()
    print len(results)
    for row in results:
        num = row[0]
        str1 = re.findall(r'([a-z]+)',num)[0]
        str2 = re.findall(r'([0-9]+)',num)[0]
        url = "http://yyk.99.com.cn/%s/%s/" % (str1, str2)
        r.rpush("hos99_spider:slave8_urls",url)
except:
    print "error"

db.close()
