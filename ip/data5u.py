# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import urllib
import socket

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

# 爬取网站 http://www.data5u.com/
def getProxyIp():
     proxy = []
     for i in range(1,2):
          try:
               url = 'http://www.data5u.com/'
               req = urllib2.Request(url,headers=header)
               res = urllib2.urlopen(req).read()
               soup = BeautifulSoup(res, 'lxml')
               ips = soup.select('li > ul.l2')
               for x in range(1,len(ips)):
                    ip = ips[x]
                    tds = ip.select('span')
                    ip_temp = tds[0].get_text()+":"+tds[1].get_text()
                    proxy.append(ip_temp)
          except:
                continue
     return proxy
# 验证ip是否可用
def validateIp(proxy):
     url = "http://ip.chinaz.com/getip.aspx"
     f = open("D:\PROJ\python\scrapy_redis\ip\ip_5u.txt","w")
     socket.setdefaulttimeout(3)
     for i in range(0,len(proxy)):
          try:
               ip = proxy[i].strip().split(":")
               proxy_host = "http://"+ip[0]+":"+ip[1]
               proxy_temp = {"http":proxy_host}
               res = urllib.urlopen(url,proxies=proxy_temp).read()
               f.write(proxy[i]+'\n')
               print proxy[i]
          except Exception,e:
                continue
     f.close()

if __name__ == '__main__':
     proxy = getProxyIp()
     validateIp(proxy)