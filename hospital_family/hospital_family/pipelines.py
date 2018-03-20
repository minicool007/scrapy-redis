# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from scrapy import log
import MySQLdb
import MySQLdb.cursors

class HospitalFamilyPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                            host="localhost",
                                            db="dbtest",
                                            user="root",
                                            passwd="123456",
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset="utf8",
                                            use_unicode=False
                                            )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tb, item):

        # tb.execute("insert into hos_family (PROVINCE, CITY, DISTRICT, HOSPITAL_NAME,NUM) \
        #             values (%s, %s, %s, %s,%s)",
        #            (item["PROVINCE"].encode('utf-8'),
        #             item["CITY"].encode('utf-8'),
        #             item["DISTRICT"].encode('utf-8'),
        #             item["HOSPITAL_NAME"].encode('utf-8'),
        #             item["NUM"].encode('utf-8')))
        tb.execute("insert into hos_detail (NUM, HOSPITAL_NAME, ALIAS, POINT_LAT, POINT_LNG, ADDRESS, TEL, TYPE, RATE, LINK, IS_HOS, NATURE) \
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (item["NUM"],
                    item["HOSPITAL_NAME"].encode('utf-8'),
                    item["ALIAS"].encode('utf-8'),
                    item["POINT_LAT"].encode('utf-8'),
                    item["POINT_LNG"].encode('utf-8'),
                    item["ADDRESS"].encode('utf-8'),
                    item["TEL"].encode('utf-8'),
                    item["TYPE"].encode('utf-8'),
                    item["RATE"].encode('utf-8'),
                    item["LINK"].encode('utf-8'),
                    item["IS_HOS"].encode('utf-8'),
                    item["NATURE"].encode('utf-8')))
    def handle_error(self, e):
        log.err(e)
