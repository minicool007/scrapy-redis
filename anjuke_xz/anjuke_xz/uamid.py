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
    {"ipaddr": "59.67.152.230:3128"},
    {"ipaddr": "159.89.141.10:8080"},
    {"ipaddr": "146.196.52.56:80"},
    {"ipaddr": "188.43.15.105:9090"},
]
