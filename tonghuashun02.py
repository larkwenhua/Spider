# _*_coding:utf-8 _*_
import time
from selenium import webdriver
import requests

# 定义浏览器对象
browser = webdriver.Chrome()
# 获取目标页面，设置等待时间，让内容加载完成
browser.get("http://q.10jqka.com.cn/thshy/detail/code/881147/")
time.sleep(5)
# 打印网页标题
print (browser.title)
# 找到元素所在的列集合-----是一个列表
# driver = browser.find_elements_by_xpath("//tbody/tr")
# print("a列表长度：%s"%len(a))
item = []

scodes = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr/td[2]/a')
snames = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr/td[3]/a')

# with open('name_code.txt', 'w', ) as f:
for i in range(len(scodes)):
    info = scodes[i].text + ':' + snames[i].text
    item.append(scodes[i].text)

browser.find_element_by_partial_link_text("下一页").click()
time.sleep(5)
scodes = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr/td[2]/a')
snames = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr/td[3]/a')
for i in range(len(scodes)):
    info = scodes[i].text + ':' + snames[i].text

    item.append(scodes[i].text)

browser.find_element_by_partial_link_text("下一页").click()
time.sleep(5)
scodes = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr/td[2]/a')
snames = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr/td[3]/a')
for i in range(len(scodes)):
    info = scodes[i].text + ':' + snames[i].text
    item.append(scodes[i].text)

print("环保工程公司总数:%s"%len(item))



num = 1
for i in item:

    export = "debt"
    type = ["year", "simple", "report"]

    for t in type:
        print("------------%s------------------" % num)
        num += 1
        type = t
        code = i
        url = 'http://basic.10jqka.com.cn/api/stock/export.php?export={}&type={}&code={}'.format(export, type, code)

        browser.get(url)
        time.sleep(2)
        print("download:%s---%s"%(code, type))
        print("--------------over---------------")
browser.quit()






