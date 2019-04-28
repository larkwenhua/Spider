#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/9 13:33
# @Author  : Py.qi
# @File    : JD.py
# @Software: PyCharm
import re

import requests
import pymongo
from pyquery import PyQuery as pq

# client=pymongo.MongoClient('192.168.122.88',port=6379)
# db=client['JD']

def page_parse(html):
    doc=pq(html,parser='html')
    items=doc('#J_goodsList .gl-item').items()
    for item in items:
        if item('.p-img img').attr('src'):
            image=item('.p-img img').attr('src')
        else:
            image=item('.p-img img').attr('data-lazy-img')
        texts={
            'image':'https:'+image,
            'price':item('.p-price').text()[:6],
            'title':re.sub('\n','',item('.p-name').text()),
            'commit':item('.p-commit').text()[:-3],

        }
        yield texts

# def save_to_mongo(data):
#     if db['jd_collection'].insert(data):
#         print('保存到MongoDB成功',data)
#     else:
#         print('MongoDB存储错误',data)

def main(number):
    url='http://192.168.146.140:8050/render.html?url=https://search.jd.com/Search?keyword=python&page={}&wait=1&images=0'.format(number)
    response=requests.get(url)
    data=page_parse(response.text)
    for i in data:
        save_to_mongo(i)
        #print(i)

if __name__ == '__main__':
    for number in range(1,200,2):
        print('开始抓取第{}页'.format(number))
        main(number)