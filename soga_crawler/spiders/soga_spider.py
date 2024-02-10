# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 23:32:13 2021

@author: hp
"""
import scrapy
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
        for url in urls:
            request = scrapy.Request(url, callback=self.auction_page)
            yield request
                
        # for ta in response.xpath("//div[@class='consultants_list_data']//div[@class='item']"):
        #     item = Tax_Advisor()
        #     item['name']= ta.xpath("./h2/a/span/text()").get()
        #     item['location']=ta.xpath("./div[@class='infos']/div[@class='inside']/div[@class='place']/text()").get()
        #     item['location']=item['location'] and item['location'].replace('\r', '').replace('\t', '').replace('\n', '')
        #     item['phone_number']=ta.xpath("./div[@class='infos']/div[@class='inside']/div[@class='phone']/text()").get()
        #     item['phone_number']=item['phone_number'] and item['phone_number'].replace('\r', '').replace('\t', '').replace('\n', '')
        #
        #     item['email_address']=ta.xpath("./div[@class='infos']/div[@class='inside']/div[@class='email']/a/text()").get()
        #     print(item)
        #     yield item

        
    def auction_page(self, response):
        pass
        
        