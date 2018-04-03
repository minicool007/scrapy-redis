# -*- coding: utf-8 -*-#
import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 代理
class Uamid(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        thisua = random.choice(UPPOOL)
        print("当前使用User-Agent是："+thisua)
        request.headers.setdefault('User-Agent',thisua)

UPPOOL = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
    ]
# ip
class HTTPPROXY(HttpProxyMiddleware):
    # 初始化 注意一定是 ip=''
    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):

        item = random.choice(IPPOOL)
        try:
            print("当前的IP是："+item["ipaddr"])
            request.meta["proxy"] = "http://"+item["ipaddr"]
        except Exception as e:
            print(e)
            pass

# 设置IP池
IPPOOL = [
    {"ipaddr": "114.237.26.126:45521"},
    {"ipaddr": "59.52.187.240:48159"},
    {"ipaddr": "220.162.155.100:23115"},
    {"ipaddr": "123.162.192.101:20412"},
    {"ipaddr": "222.89.82.15:24774"},
    {"ipaddr": "180.155.132.34:40599"},
    {"ipaddr": "183.164.239.177:46779"},
    {"ipaddr": "36.27.140.59:20786"},
    {"ipaddr": "115.221.113.21:31331"},
    {"ipaddr": "117.86.9.42:40989"},
    {"ipaddr": "117.95.105.96:29653"},
    {"ipaddr": "123.53.119.197:23047"},
    {"ipaddr": "123.163.162.120:26003"},
    {"ipaddr": "180.122.150.233:40792"},
    {"ipaddr": "117.28.160.117:33894"},
    {"ipaddr": "113.89.84.161:22804"},
    {"ipaddr": "171.12.227.153:32591"},
    {"ipaddr": "123.53.132.155:32648"},
    {"ipaddr": "60.184.118.80:29049"},
    {"ipaddr": "113.121.187.0:23682"},

]
