# -*- coding: utf-8 -*-
import requests
import json
import demjson
import jsonpath
import time
import os



curPath = 'E:\上市公司年度报表'
if not os.path.exists(curPath):
    os.makedirs(curPath)


decode_all =[
'000998',

]

decode_alltmp=['600784']
for decode in decode_all:


    urls = [
        'http://basic.10jqka.com.cn/api/stock/finance/%s_cash.json' % decode,
        'http://basic.10jqka.com.cn/api/stock/finance/%s_benefit.json' % decode,
        'http://basic.10jqka.com.cn/api/stock/finance/%s_debt.json' % decode,
        ]
    for url in urls:
        try:
            time.sleep(1)
            headers = {

                'Host': 'basic.10jqka.com.cn',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
            }
            data = requests.get(url, headers=headers).text.replace('\\\\', '\\')
            print(data+"999")

            # 异常处理，并记录为匹配到的公司

            json_data = demjson.decode(data)


            #f
            # # year\simple\report 数据
            a = jsonpath.jsonpath(json_data, expr='$..flashData')
            # #未知数据
            # b = jsonpath.jsonpath(json_data, expr="$..fieldflashData")
            a1 = str(a).replace("['", "").replace("']", "")
            a2 = json.loads(a1)
            title = a2['title']
            report = a2['report']
            year = a2["year"]
            simple = a2["simple"]
            type = url.split('_')[-1].replace('.json', '')
            # 月度数据报表写入文件
            filename_simple = curPath + os.path.sep + "%s_" % decode + type + '_year.txt'
            with open(filename_simple, 'w') as f:
                for i in range(0, len(title)):
                    year_data = str(title[i]) + str(year[i])
                    # simple_data = str(title[i]) + str(simple[i])
                    # print(year_data)

                    f.write(year_data + "\n")
                f.close()

        except Exception as f:

            print('查不到%s数据' % decode)
            error = r'E:/ERROR.txt'
            with open(error, 'w') as f_error:
                f_error.write(decode + "\n")
                f_error.close()


        #年度数据报表
        # for i in range(0, len(title)):
        #     year_data = str(title[i]) + str(year[i])
        #     print(year_data)






        # 报告期数报表
        # for i in range(0, len(title)):
        #     repport_data = str(title[i]) + str(report[i])
        #     print(repport_data)
        #






