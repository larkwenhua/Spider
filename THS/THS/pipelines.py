# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import demjson
import jsonpath
import json

class ThsPipeline(object):
    def process_item(self, item, spider):

        code_info = str(item["code_info"]).split('/')[-2]
        industry_info = str(item['industry_info']).replace(':', "")
        # 创建文件夹
        curPath = './data'
        codePath = code_info
        namePath = industry_info
        # print(tempPath)
        targetPath = curPath + os.path.sep + codePath + os.path.sep + namePath

        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        #解析连接，数据提取
        industry_number = item['industry_number']
        print('---------%s--------'%industry_number)
        urls = [
            'http://basic.10jqka.com.cn/api/stock/finance/%s_cash.json' % industry_number,
            'http://basic.10jqka.com.cn/api/stock/finance/%s_benefit.json' %industry_number,
            'http://basic.10jqka.com.cn/api/stock/finance/%s_debt.json' %industry_number,
        ]
        for url in urls:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
            data = requests.get(url, headers=headers).text.replace('\\\\', '\\')
            json_data = demjson.decode(data)

            # year\simple\report 数据
            a = jsonpath.jsonpath(json_data, expr='$..flashData')
            # #未知数据
            # b = jsonpath.jsonpath(json_data, expr="$..fieldflashData")
            a1 = str(a).replace("['", "").replace("']", "")
            a2 = json.loads(a1)
            title = a2['title']
            report = a2['report']
            year = a2["year"]
            simple = a2["simple"]
            # 年度数据报表
            type = url.split('_')[-1].replace('.json', '')
            filename_year = targetPath + os.path.sep + type + '_year.txt'
            with open(filename_year, 'w') as f:
                for i in range(0, len(title)):
                    year_data = str(title[i]) + str(year[i])
                    # print(year_data)
                    f.write(year_data + "\n")
            # 月度数据报表
            filename_simple = targetPath + os.path.sep + type + '_simple.txt'
            with open(filename_simple, 'w') as f:
                for i in range(0, len(title)):
                    simple_data = str(title[i]) + str(simple[i])
                    f.write(simple_data + "\n")
                # print(simple_data)
            # 报告期数报表
            filename_report = targetPath + os.path.sep + type + '_report.txt'
            with open(filename_report, 'w') as f:
                for i in range(0, len(title)):
                    report_data = str(title[i]) + str(report[i])
                    # print(report_data)
                    f.write(report_data + "\n")


        return item