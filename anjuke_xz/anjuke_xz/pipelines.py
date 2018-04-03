# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class AnjukeXzPipeline(object):
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
        # tb.execute("insert into xzAnjuke ( CITY, DISTRICT, RES_NAME,NUM, BUILD_AREA) \
        #             values (%s, %s, %s, %s, %s)",
        #            (item["CITY"],
        #             item["DISTRICT"],
        #             item["RES_NAME"],
        #             item["NUM"],
        #             item["BUILD_AREA"]))
        tb.execute("insert into xzAnjuke_detail (NUM, RES_NAME, DISTRICT, RES_ID, POINT, ADRESS, MANAGE_COMPANY, \
                MANAGE_FEE, GREEN, VOLUM, DEVELOPER, NEW_SALE, SUCCESS_TIME, PARK_NUM, PARK_RATE, \
                USED_TIME, MANAGE_TYPE, BUILD_TYPE, PLAN_NUM, STATE, PROCCEED, LINK) \
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (item["NUM"],
                    item["RES_NAME"],
                    item["DISTRICT"],
                    item["RES_ID"],
                    item["POINT"],
                    item["ADRESS"],
                    item["MANAGE_COMPANY"],
                    item["MANAGE_FEE"],
                    item["GREEN"],
                    item["VOLUM"],
                    item["DEVELOPER"],
                    item["NEW_SALE"],
                    item["SUCCESS_TIME"],
                    item["PARK_NUM"],
                    item["PARK_RATE"],
                    item["USED_TIME"],
                    item["MANAGE_TYPE"],
                    item["BUILD_TYPE"],
                    item["PLAN_NUM"],
                    item["STATE"],
                    item["PROCCEED"],
                    item["LINK"]))

    def handle_error(self, e):
        print e

