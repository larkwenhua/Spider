# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os

class DataPipeline(object):
    def process_item(self, item, spider):
        curPath = './data'

        if not os.path.exists(curPath):
            os.makedirs(curPath)
        filename_path = curPath + os.path.sep + item['title'] + '.txt'
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(str(item['content']) + "\n")
        return item







