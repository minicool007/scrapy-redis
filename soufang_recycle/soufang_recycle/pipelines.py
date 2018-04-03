# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class SoufangRecyclePipeline(object):
    def process_item(self, item, spider):
        return item

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
        # tb.execute("insert into sfrecycle (CITY, DISTRICT, RES_NAME, NUM, BUILD_YEAR, LINK) \
        #             values (%s, %s, %s, %s, %s, %s)",
        #            (item['CITY'],
        #             item["DISTRICT"],
        #             item["RES_NAME"],
        #             item["NUM"],
        #             item["BUILD_YEAR"],
        #             item["LINK"]))
        tb.execute("insert into sfrecycle_detail (NUM,	RES_ID,RES_NAME,	POINT,	ADDRESS,	LOCATION,	BUILD_YEAR,	\
                 MANAGE_TYPE,	DESCRIPTION,	BUILD_STRUCTURE,	BUILD_TYPE,MANAGE_COMPANY,	MANAGE_LOCATION,	MANAGE_TEL,	\
                 MANAGE_FEE,	INFO,	BUILD_AREA,	AREA,	GREEN,	VOLUM,	DEVELOPER,	OPEN_TIME,	SUCCESS_TIME,	PARK,SCHOOL,HOUSE_NUM,RENT_NUM,LINK) \
                values (%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s,	%s, %s)",
                   (item['NUM'],
                    item['RES_ID'],
                    item['RES_NAME'],
                    item['POINT'],
                    item['ADDRESS'],
                    item['LOCATION'],
                    item['BUILD_YEAR'],
                    item['MANAGE_TYPE'],
                    item['DESCRIPTION'],
                    item['BUILD_STRUCTURE'],
                    item['BUILD_TYPE'],
                    item['MANAGE_COMPANY'],
                    item['MANAGE_LOCATION'],
                    item['MANAGE_TEL'],
                    item['MANAGE_FEE'],
                    item['INFO'],
                    item['BUILD_AREA'],
                    item['AREA'],
                    item['GREEN'],
                    item['VOLUM'],
                    item['DEVELOPER'],
                    item['OPEN_TIME'],
                    item['SUCCESS_TIME'],
                    item['PARK'],
                    item['SCHOOL'],
                    item['HOUSE_NUM'],
                    item['RENT_NUM'],
                    item['LINK']))


    def handle_error(self, e):
        print e
