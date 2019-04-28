# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

class DoubamovieSpider(scrapy.Spider):
    name = "doubanmovie"
    allowed_domains = ["movie.top250.com"]
    offset = 0
    url = "https://movie.top250.com/top250?start="
    start_urls = (
            url+str(offset),
    )

    def parse(self, response):

        item = DoubanItem()
        movies = response.xpath("//div[@class='info']")
        # ll = ItemLoader(item=DoubanItem(), response=response)
        for each in movies:
            # 测试用例
            # each.ll.add_xpath('title', './/span[@class="title"][1]/text()'.extract()[0])
            # each.ll.add_xpath('bd', './/div[@class="bd"]/p/text()'.extract()[0])
            # each.ll.add_xpath('start', './/div[@class="star"]/span[@class="rating_num"]/text()'.extract()[0])
            # each.ll.add_xpath('quote', './/p[@class="quote"]/span/text()'.extract()[0])

            # 标题
            item['title'] = each.xpath(".//span[@class='title'][1]/text()").extract()[0]
            # 信息
            item['bd'] = each.xpath(".//div[@class='bd']/p/text()").extract()[0]
            # 评分
            item['star'] = each.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract()[0]
            # 简介
            quote = each.xpath(".//p[@class='quote']/span/text()").extract()
            if len(quote) != 0:
                item['quote'] = quote[0]
            yield item

        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url + str(self.offset), callback = self.parse)


