# -*- coding: utf-8 -*-
import requests

from lxml import etree
#请输入查询公司代码
gs = 600008

url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{}/ctrl/2018/displaytype/4.phtml'.format(str(gs))
headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}
# proxy_list = [
# #     "60.2.37.198:49565",
# #     ]
# proxy_ip = random.choice(proxy_list) #随机获取代理ip
# proxies = {'http': proxy_ip}
response = requests.get(url, headers=headers)
#data = response.content.xpath("/html/body/div[1]/div[9]/div[2]/div/div[3]/table[2]/tbody/tr/td")
response.encoding = "gbk"

# 将request.content 转化为 Element
data = etree.HTML(response.content)
#获取项目名称
titles = data.xpath("//table[2]/tbody/tr/td/a/text()")
titles.insert(0, "报告日期")
titles.insert(35, "四、汇率变动对现金及现金等价物的影响")
titles.insert(36, "五、现金及现金等价物净增加额")
titles.insert(38, "六、期末现金及现金等价物余额")
#69
print(len(titles))
# #匹配数据
lists = data.xpath("//table[2]/tbody/tr")

dict = {}
i = 0
for each in lists:
    list = each.xpath("td/text()")
    if len(list) > 0:
        dict[titles[i]] = list
        i += 1
periods =dict["报告日期"]
del dict["报告日期"]

for i in range(0, len(periods)):
    period = periods[i]
    j = 1
    for item in dict.values():
        info = str(gs) + "-"*4 + period.replace("-", "") + "-"*4 +titles[j] + "-"*4 + str(item[i]).replace("--", "0")
        j += 1
        print(info)





