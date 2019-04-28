# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os


class DoubanPipeline(object):

    def __init__(self):
        Path = './date'
        if not os.path.exists(Path):
            os.makedirs(Path)
        # 创建一个文件

        self.filename = codecs.open("./date/top.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        # 中文默认使用ascii码来存储，禁用后默认为Unicode字符串
        content = json.dumps(dict(item), ensure_ascii=False) + "\n"
        print(content)
        print("******************************")
        self.filename.write(content)
        return item

    def close_spider(self, spider):
        self.filename.close()

