# -*- coding: utf-8 -*-

# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import sys
# import os
# curPath = os.path.abspath(os.path.dirname(__file__))
# print(curPath)
# Path = os.path.split(curPath)[0]
# rootPath = os.path.split(Path)[0]
# print(rootPath)
# print('^^^^^^^^^^^'*10)
# sys.path.append(rootPath)

from WenShu import settings
from pymongo import MongoClient
from .settings import HOST, NAME, PORT, SHEET
class WenshuPipeline(object):

    def __init__(self):
        # 初始化数据库连接
        #mongodb
        # 获取setting主机名、端口号和数据库名
        host = HOST
        port = PORT
        db_name = NAME
        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = MongoClient(host=host, port=port)
        # 指向指定的数据库
        mdb = client[db_name]
        # 获取数据库里存放数据的表名
        self.post = mdb[SHEET]
        # oracle
        # /////////

    def process_item(self, item, spider):
        # 插入数据到mongodb
        data = dict(item)
        # 向指定的表里添加数据
        self.post.insert(data)

        # 插入数据到Oracle
        # pass

        return item
