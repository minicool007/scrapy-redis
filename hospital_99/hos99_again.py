# -*- coding: utf-8 -*-
import xlrd
import xlwt
import json
import urllib,urllib2
import datetime
import re
import sys
from xlutils.copy import copy
from bs4 import BeautifulSoup
import time

reload(sys)
sys.setdefaultencoding('utf-8')

# 加入是否医保字段

# 读取excel 在后面追加两列
# http://api.map.baidu.com/geocoder/v2/?address=%E5%8C%97%E4%BA%AC%E5%B8%82%E6%B5%B7%E6%B7%80%E5%8C%BA%E4%B8%8A%E5%9C%B0%E5%8D%81%E8%A1%9710%E5%8F%B7&output=json&ak=ycsGLpxUZ4OCRVDpqicGAD9gzqARQORZ&callback=showLocation

path_in = r"F:\data\hos99.xlsx"
path_out = r"F:\data\hos99_1.xlsx"

def read_excel(file_in):
    list = []

    for sheet in file_in.sheets():
        print sheet.name, sheet.nrows, sheet.ncols
        url_list = []
        lrow = sheet.nrows
        # 获取第10列
        for i in range(1, lrow):
            link = sheet.cell(i, 9).value + "jianjie.html"
            link = unicode(link)
            url_list.append(link)
        dict1 = {'sname': sheet.name, 'srow': sheet.nrows - 1, 'url_list': url_list}
        list.append(dict1)
    return list


if __name__=='__main__':
    file_in = xlrd.open_workbook(path_in)
    print file_in.sheet_names()
    # 读取文件内容
    list = read_excel(file_in)
    # 打开文件，向文件里面写数据
    wfile = copy(file_in)

    for point_i in range(0, len(list)):
        w_sheet = wfile.get_sheet(point_i)
        add_1 = 11
        w_sheet.write(0, add_1, 'is_hos')
        url_list = list[point_i]['url_list']
        for num in range(0, len(url_list)):
            print num
            # 请求官网坐标
            xx = url_list[num].encode('utf-8')
            xx = xx.replace(' ', '%20')
            xx = xx.replace(' ', '%20')
            req_ = urllib2.Request(xx)
            try:
                response = urllib2.urlopen(req_)
                response = response.read()
            except:
                print "空格问题"+xx
                continue
            soup = BeautifulSoup(response, 'html.parser')
            # CSS选择器
            enter = soup.select('td.tdr.lasttd')
            if len(enter) == 3:
                is_hos = enter[2].text.strip()
                w_sheet.write(num + 1, add_1, is_hos)
                # print is_hos
            else:
                print "医保出现问题"+url_list[num]
                w_sheet.write(num + 1, add_1, "")
    wfile.save(path_out)