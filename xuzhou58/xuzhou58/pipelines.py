# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

class Xuzhou58Pipeline(object):
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
        # tb.execute("insert into xz58 (CITY, DISTRICT, COMUNITY_NAME, ALIAS, NUM) \
        #             values (%s, %s, %s, %s,%s)",
        #            (item["CITY"],
        #             item["DISTRICT"],
        #             item["COMUNITY_NAME"],
        #             item["ALIAS"],
        #             item["NUM"]))
        tb.execute("insert into xz58_detail (NUM, POINT, ADDRESS, USED_TIME, TYPE, BUILD_TIME, \
                BUILD_TYPE, MANAGE_COMPANY, MANAGE_FEE, DEVELOPER, BUILD_AREA, AREA, GREEN, VOLUM, PARK, \
                DESCRIPTION, HOUSE_NUM, RENT_NUM, LINK, COM_ID) \
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (item["NUM"],
                    item["POINT"],
                    item["ADDRESS"],
                    item["USED_TIME"],
                    item["TYPE"],
                    item["BUILD_TIME"],
                    item["BUILD_TYPE"],
                    item["MANAGE_COMPANY"],
                    item["MANAGE_FEE"],
                    item["DEVELOPER"],
                    item["BUILD_AREA"],
                    item["AREA"],
                    item["GREEN"],
                    item["VOLUM"],
                    item["PARK"],
                    item["DESCRIPTION"],
                    item["HOUSE_NUM"],
                    item["RENT_NUM"],
                    item["LINK"],
                    item["COM_ID"]))

    def handle_error(self, e):
        print e
