# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
# 导入proxies.py中的Proxies类
from .spiders.proxies import Proxies

# 实例化这个类，并调用类函数，获取代理ip
item = Proxies()
IP_POOL = item.proxies
# 为列表类型
print(item.proxies)
print("%%%%%%%%%%%%%%%%%%%"*5)
# 设置随机请求头
class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        print("+==================+")
        print(agent)

# 设置随机代理IP
class ProxyMiddleware(HttpProxyMiddleware):
    # 初始化方法
    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        ip = random.choice(IP_POOL)
        try:
            print("当前的IP是：" + ip)
            request.meta["proxy"] = ip
        except Exception as e:
            print(e)
            pass





