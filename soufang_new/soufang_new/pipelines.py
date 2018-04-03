# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class SoufangNewPipeline(object):
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
        # tb.execute("insert into xzSoufang ( CITY, DISTRICT, RES_NAME,NUM) \
        #             values (%s, %s, %s, %s)",
        #            (item["CITY"],
        #             item["DISTRICT"],
        #             item["RES_NAME"],
        #             item["NUM"]))
        tb.execute("insert into xzSoufang_detail (NUM, RES_NAME, RES_ID, POINT, ADDRESS, MANAGE_TYPE, BUILD_TYPE, \
                USED_YEAR, LOCATION, DEVELOPER, OPEN_TIME, SUCCESS_TIME, SALE_STATE, SALE_ADDRESS, MANAGE_COMPANY,MANAGE_FEE, \
                MANAGE_DESC, BUILD_AREA, AREA, GREEN, VOLUM, PARK, BUILD_NUM, HOUSE_NUM, STATE, DESCRIPT, LINK) \
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (item["NUM"],
                    item["RES_NAME"],
                    item["RES_ID"],
                    item["POINT"],
                    item["ADDRESS"],
                    item["MANAGE_TYPE"],
                    item["BUILD_TYPE"],
                    item["USED_YEAR"],
                    item["LOCATION"],
                    item["DEVELOPER"],
                    item["OPEN_TIME"],
                    item["SUCCESS_TIME"],
                    item["SALE_STATE"],
                    item["SALE_ADDRESS"],
                    item["MANAGE_COMPANY"],
                    item["MANAGE_FEE"],
                    item["MANAGE_DESC"],
                    item["BUILD_AREA"],
                    item["AREA"],
                    item["GREEN"],
                    item["VOLUM"],
                    item["PARK"],
                    item["BUILD_NUM"],
                    item["HOUSE_NUM"],
                    item["STATE"],
                    item["DESCRIPT"],
                    item["LINK"]))

    def handle_error(self, e):
        print e
