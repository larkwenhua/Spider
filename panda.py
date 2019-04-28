from bs4 import BeautifulSoup
from lxml import etree
a = open("D:\\Users\\User\Desktop/a.html", "r", encoding="utf-8")
b = a.read()
# list = []
# soup = soup = BeautifulSoup(b,'lxml')
# a = soup.find_all("dt", class_="item_right")
# b = soup.find_all("dt", class_="item")
# print(a)
# print(b)
#
# for i, j in zip(a, b):
#     list.append(j)
#     list.append(i)
# aaa = soup.find_all("dd", class_="result")
# for i,j in zip(list,aaa):
#     print(i.get_text()+j.get_text())
#



html = etree.HTML(b)
c = html.xpath("//dl/dt/text()|//dl/dd/text()")
for i in c:

    print(i.replace(" ", ""))
