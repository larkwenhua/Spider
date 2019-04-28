# -*- coding: utf-8 -*-
import scrapy
import re

from Fiction.items import FictionItem
from scrapy.http import Request

import sys
reload(sys)
sys.setdefaultencoding("utf-8")



class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['quanshuwang.com']
    start_urls = [
        'http://www.quanshuwang.com/list/1_2.html',
        # 'http://www.quanshuwang.com/list/1_3.html',
        # 'http://www.quanshuwang.com/list/1_4.html',
        # 'http://www.quanshuwang.com/list/1_5.html',
        # 'http://www.quanshuwang.com/list/1_6.html',
        # 'http://www.quanshuwang.com/list/1_7.html',
        # 'http://www.quanshuwang.com/list/1_8.html',
        # 'http://www.quanshuwang.com/list/1_9.html',
        # 'http://www.quanshuwang.com/list/1_10.html',

     ]

    def parse(self, response):
        book_urls = response.xpath('//li/a[@class="l mr10"]/@href').extract()
        for book_url in book_urls:

            #print('-------------1---------------')
            yield Request(book_url, callback=self.parse_read)

        # 获取马上阅读按钮的URL，进入章节目录

    def parse_read(self, response):
        read_url = response.xpath('//a[@class="reader"]/@href').extract()[0]
        #print('-------------2---------------')
        yield Request(read_url, callback=self.parse_chapter)

        # 获取小说章节的URL

    def parse_chapter(self, response):
        chapter_urls = response.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
        for chapter_url in chapter_urls:
           # print('-------------3---------------')
            yield Request(chapter_url, callback=self.parse_content)

        # 获取小说名字,章节的名字和内容

    def parse_content(self, response):
        # 小说名字
        print('---------------4----------------')
        name = response.xpath('//div[@class="main-index"]/a[@class="article_title"]/text()').extract_first()

        result = response.text
        # 小说章节名字
        chapter_name = response.xpath('//strong[@class="l jieqi_title"]/text()').extract_first()
        # 小说章节内容
        chapter_content_reg = r'style5\(\);</script>(.*?)<script type="text/javascript">'

        chapter_content_2 = re.findall(chapter_content_reg, result, re.S)[0]

        chapter_content_1 = chapter_content_2.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '')

        chapter_content = chapter_content_1.replace('<br />', '')
        print(chapter_content)


        item = FictionItem()
        item['name'] = name
        item['chapter_name'] = chapter_name
        item['chapter_content'] = chapter_content
        yield item


