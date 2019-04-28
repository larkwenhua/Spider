# -*- coding: utf-8 -*-
import scrapy
from CountryData.items import CountrydataItem
import re


class DataSpider(scrapy.Spider):
    name = 'data'
    allowed_domains = ['www.offcn.com']
    page = 2
    url = 'http://www.offcn.com/xingce/mryl/'
    start_urls = [url + str(page)+ '.html',]
    print('-------------------')
    # print(start_urls)
    print('-------------------')
    def parse(self, response):
        #父页面标题和链接
        titleUrl = response.xpath('/html/body/div/div/dl/dt/a/@href').extract()

        for item in titleUrl:
            yield scrapy.Request(url=item, callback=self.s_parse)
    def s_parse(self, response):
    # 子页面标题、内容
        content = response.xpath('/html/body/div[4]/div[1]/div/div[3]/p/text()').extract()
        title = response.xpath('/html/body/div[4]/div[1]/div/h1/text()').extract_first()
        # print(title)
        # print(content)
        #实例化对象
        item = CountrydataItem()

        item['title'] = title
        #用正则匹配字段
        re_date = re.compile(r'\d+')
        date = re_date.findall(str(title))
        item['date'] = date
        #删除列表元素
        del content[1]
        #列表转字符串
        content = ''.join(content)
        item['content'] = content

        yield item
        #构造处理下一页请求
        if self.page < 156:
            self.page += 1
            yield scrapy.Request(url=self.url + str(self.page) + '.html' , callback=self.parse)


