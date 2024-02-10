# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 23:32:13 2021

@author: hp
"""
import scrapy
import uuid

from scrapy.loader import ItemLoader
from soga_crawler.items import Aukcia,Dielo

class SogaSpider(scrapy.Spider):
    name = "soga_spider"
    allowed_domains = ["www.soga.sk"]
    start_urls = (
        "https://www.soga.sk/aukcie-obrazy-diela-umenie-starozitnosti/aukcie/zoznam-aukcii",
    )

    def parse(self, response):
        urls = response.xpath("//div[@id='auctionsList']/div[@class='item']/h2/a/@href").extract()
        urls=['https://www.soga.sk'+x for x in urls]
        
        # for url in urls:
        #     print(url)
        for url in urls[0:1]:
            print(f'{url}')
            request = scrapy.Request(url, callback=self.auction_main_page)
            yield request

        
    def auction_main_page(self, response):
            item = Aukcia()
            item['id']= str(uuid.uuid4())
            item['nazov']=str(response.xpath("//div[@id='auction']/div[@class='auctionSlide']/div[@class='imgInfoWrapper']/div[@class='imgInfoContent']/text()").get())
            item['datum']=str(response.xpath("//div[@id='auction']/div[@class='auctionSlide']/div[@class='imgInfoWrapper']/div[@class='imgInfoContent']/p[@class='date']/text()").get())
            item['popis']=str(response.xpath("//div[@id='auction']/div[@class='auctionSlide']/div[@class='text']/text()").extract())
            item['url']=response.url

            print(item)
            yield item
        