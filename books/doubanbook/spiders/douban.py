# -*- coding: utf-8 -*-
import scrapy
from doubanbook.items import DoubanbookItem
import sys
    #reload(sys)
    #sys.setdefaultencoding('utf-8')

class DoubanSpider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['read.top250.com']
    url = 'https://read.top250.com/kind/1?start='
    offset = 0
    start_urls = ['https://read.top250.com/kind/1?start=' + str(offset)]


    def parse(self, response):
    	#取每一页里的所有链接
        links = response.xpath('//div[@class="wrapper"]/div[@class="main"]/article[@class="col col10"]//div[@class="bd"]/ul[@class="list-lined ebook-list column-list"]/li[@class="item store-item"]/div[@class="info"]/div[@class="title"]/a/@href').extract()
        
        print(links)
        print("_____ssssssssssssssssssssssssssssssss______")

        #迭代取出链接
        for link in links:

        	link = 'https://read.top250.com' + link

                        
 		# 提取列表里的每个链接，发送请求放到请求队列里,并调用self.parse_item来处理
        	yield scrapy.Request(link, callback = self.parse_item)


        # 页面终止条件成立前，会一直自增offset的值，并发送新的页面请求，调用parse方法处理
        if self.offset <= 64900:
            self.offset += 20
            # 发送请求放到请求队列里，调用self.parse处理response\
            print("-------2-------")
            yield scrapy.Request(self.url + str(self.offset), callback = self.parse)


    def parse_item(self, response):
        pass

        print("-------3-------")
    	item = DoubanbookItem()

        title = response.xpath('//div[@class="article-profile-bd"]/h1/text()').extract()
        if len(title) != 0:
            item['title'] = title[0]

    	author = response.xpath(' //div[@class="article-meta"]/p[@class="author"]//a/text()').extract()
        if len(author) != 0:
            item['author'] = author[0]

    	info = response.xpath('//div[@class]/div[@class="info"]/p/text()').extract()
        if len(info) != 0:
            item['info'] = info[0]

    	item['url'] = response.url

    	yield item

    	