# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class AnjukeXiaoquPipeline(object):
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
        # tb.execute("insert into xzRecycle ( CITY, DISTRICT, RES_NAME,NUM) \
        #             values (%s, %s, %s, %s)",
        #            (item["CITY"],
        #             item["DISTRICT"],
        #             item["RES_NAME"],
        #             item["NUM"]))
        tb.execute("insert into xzrecycle_detail (NUM, RES_ID, ADDRESS, POINT, BUILD_YEAR, MANAGE_TYPE, MANAGE_COMPANY, \
                MANAGE_FEE,BUILD_AREA, GREEN, VOLUM, DEVELOPER, PARK, HOUSE_NUME, RENT_NUM, LINK ) \
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (item["NUM"],
                    item["RES_ID"],
                    item["ADDRESS"],
                    item["POINT"],
                    item["BUILD_YEAR"],
                    item["MANAGE_TYPE"],
                    item["MANAGE_COMPANY"],
                    item["MANAGE_FEE"],
                    item["BUILD_AREA"],
                    item["GREEN"],
                    item["VOLUM"],
                    item["DEVELOPER"],
                    item["PARK"],
                    item["HOUSE_NUME"],
                    item["RENT_NUM"],
                    item["LINK"]))

    def handle_error(self, e):
        print e
