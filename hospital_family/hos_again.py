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

# 部分字段抓取错误
# 坐标 官网链接

# 读取excel 在后面追加两列
# http://api.map.baidu.com/geocoder/v2/?address=%E5%8C%97%E4%BA%AC%E5%B8%82%E6%B5%B7%E6%B7%80%E5%8C%BA%E4%B8%8A%E5%9C%B0%E5%8D%81%E8%A1%9710%E5%8F%B7&output=json&ak=ycsGLpxUZ4OCRVDpqicGAD9gzqARQORZ&callback=showLocation

path_in = r"F:\data\hos_family_1.xlsx"
path_out = r"F:\data\hos_family_2.xlsx"

def read_excel(file_in):
    list = []

    for sheet in file_in.sheets():
        print sheet.name, sheet.nrows, sheet.ncols
        url_list = []
        lrow = sheet.nrows
        # 获取第5列--resblock_name和第9列address的值
        for i in range(1, lrow):
            resblock_name = sheet.cell(i, 6).value.encode('utf-8').replace('\r','').replace('\t','').replace(' ','').replace('\n','')
            resblock_name = unicode(resblock_name)
            baidu_url = "http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=wbvGOnzySKqaXT82jm5YsZSkLzQLi8Qf" % resblock_name

            link = sheet.cell(i, 10).value
            link = unicode(link)
            data = {"baidu_url":baidu_url,"link":link}
            url_list.append(data)
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
        add_1 = 14
        add_2 = 15
        w_sheet.write(0, add_1, 'point')
        w_sheet.write(0, add_2, 'url')
        url_list = list[point_i]['url_list']
        for num in range(13947, len(url_list)):
            print num
            # 请求百度坐标
            # print(datetime.datetime.now())
            xx = url_list[num]["baidu_url"].encode('utf-8')
            xx = xx.replace(' ','')
            req = urllib2.Request(xx)
            try:
                res = urllib2.urlopen(req)
                res = res.read()
            except:
                print "问题1" +xx
                continue

            # str转化成 dict
            result = json.loads(res)
            if result['status'] == 0:
                data = result['result']['location']
                w_sheet.write(num + 1, add_1, str(data['lng'])+","+str(data['lat']))
                # print str(data['lng'])+","+str(data['lat'])
            else:
                w_sheet.write(num + 1, add_1, '')
            # 请求官网坐标
            # print url_list[num]["link"]
            req_ = urllib2.Request(url_list[num]["link"].encode('utf-8'))
            try:
                response = urllib2.urlopen(req_)
                response = response.read()
            except:
                print "问题4"+url_list[num]["link"]
                continue
            soup = BeautifulSoup(response, 'html.parser')
            # CSS选择器
            enter = soup.select('div.introPic > dl > dd > a.telA')
            if len(enter) != 0:
                try:
                    pre = str(enter[0].get('onclick')).split("'")
                    last = pre[1]
                except:
                    print "问题2"+url_list[num]["link"]
                w_sheet.write(num + 1, add_2, last.decode("utf8"))
            else:
                w_sheet.write(num + 1, add_2, "")
                print "问题3" + url_list[num]["link"]
    wfile.save(path_out)