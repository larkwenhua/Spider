# -*- coding: utf-8 -*-

import os

class FictionPipeline(object):

    def process_item(self, item, spider):
        curPath = './date'

        tempPath = item['name']
        print(tempPath)
        targetPath = curPath + os.path.sep + tempPath
        print('*********************************************')
        print(targetPath)
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        filename_path = curPath + os.path.sep + item['name'] + os.path.sep + str(item['chapter_name']) + '.txt'
        with open(filename_path, 'w') as f:
            f.write(item['chapter_content'] + "\n")
        return item
