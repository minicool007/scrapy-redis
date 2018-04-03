# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import urllib
import socket

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

# 爬取网站 http://www.xicidaili.com/nn/
def getProxyIp():
     proxy = []
     path_in = "D:\PROJ\python\scrapy_redis\ip\ip_xici.txt"
     with open(path_in, 'r') as file_to_read:
          while True:
               lines = file_to_read.readline()
               if not lines:
                    break
               proxy.append(lines.strip())
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

               f.write('{"ipaddr": "'+proxy[i]+'"},'+'\n')
               print proxy[i]
          except Exception,e:
                continue
     f.close()

if __name__ == '__main__':
     proxy = getProxyIp()
     validateIp(proxy)