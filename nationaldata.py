# _*_coding:utf-8 _*_
import os
import time
import requests
import io



t = time.time()
timestamp = int(round(t * 1000))
PARS = [
    "A0601",
    # "A021M02", "A021M03", "A021M04", "A021M05", "A021M06", "A021M07", "A021M08",
    # "A021M09", "A021M19", "A021M1A", "A021M2A", "A021M2B", "A021M2C", "A021M2D", "A021M2E",
    # "A021M2F", "A021M2G", "A021M2H", "A021M2I"
]
NAMES = {
    "A0601":"工业企业单位数",

    # "A021M02":"工业亏损企业单位数", "A021M03":"工业企业流动资产合计",
    # "A021M04":"工业企业应收账款","A021M05":"工业企业存货", "A021M06":"工业企业产成品存货",
    # "A021M07":"工业企业资产总计", "A021M08":"工业企业负债合计", "A021M09":"工业企业营业收入",
    # "A021M19":"工业企业主营业务收入", "A021M1A":"工业企业营业成本", "A021M2A":"工业企业主营业务成本",
    # "A021M2B":"工业企业主营业务税金及附加", "A021M2C":"工业企业销售费用", "A021M2D":"工业企业管理费用",
    # "A021M2E":"工业企业财务费用", "A021M2F":"工业企业利息支出", "A021M2G":"工业企业利润总额",
    # "A021M2H":"工业企业亏损总额", "A021M2I":"工业企业应缴增值税"
         }
# for par in PARS:

    # print(NAMES['%s' %par])


path = './data'
if not os.path.exists(path):
    os.makedirs(path)

for par in PARS:

    m = 'QueryData'
    dbcode = 'hgyd'
    rowcode = 'zb'
    colcode = 'sj'
    wds = '[]'
    dfwds = '[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"2013-2014"}]' % par

    url = 'http://data.stats.gov.cn/easyquery.htm?m={}&dbcode={}&rowcode={}&colcode={}&wds={}&dfwds={}&k1={}'.format(
        m, dbcode, rowcode, colcode, wds, dfwds, timestamp)
    response = requests.get(url)
    tt = (NAMES['%s' %par])
    print (tt)
    print(response.text)
    filename = path + os.path.sep + NAMES['%s' %par]+".json"
    print (filename)
    # with open(filename, 'w',) as f:
    #
    #     f.write(response.text)
    #     f.close()
    print("working ")
print("--------------over------------")


