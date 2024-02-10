# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 23:32:13 2021

@author: hp
"""
import scrapy
import uuid
import ast
import hashlib


from scrapy.loader import ItemLoader
from soga_crawler.items import Aukcia, Dielo

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
            print(f'{url}')
            request = scrapy.Request(url, callback=self.auction_main_page)
            yield request

        
    def auction_main_page(self, response):
            aukcia = Aukcia()
            aukcia['id']= str(uuid.uuid4())
            aukcia['nazov']=str(response.xpath("//div[@id='auction']/div[@class='auctionSlide']/div[@class='imgInfoWrapper']/div[@class='imgInfoContent']/text()").get())
            aukcia['datum']=str(response.xpath("//div[@id='auction']/div[@class='auctionSlide']/div[@class='imgInfoWrapper']/div[@class='imgInfoContent']/p[@class='date']/text()").get())
            aukcia['popis']=' '.join(ast.literal_eval(str(response.xpath("//div[@id='auction']/div[@class='text']//text()").extract())))
            aukcia['url']=response.url

            #print(aukcia)
            yield aukcia

            urls=[response.url+'?page='+str(x+1) for x in range(50)]

            # for url in urls:
            #     print(url)
            for url in urls:
                request = scrapy.Request(url, callback=self.auction_page, meta={'auction_id': aukcia['id']})
                yield request

    def auction_page(self, response):

            urls=response.xpath("//div[@id='auctionArtworks']/div[@class='item']/h2/a/@href").extract()
            urls = ['https://www.soga.sk' + x for x in urls]

            # for url in urls:
            #     print(url)
            for url in urls:
                request = scrapy.Request(url, callback=self.artwork_page, meta={'auction_id': response.meta['auction_id']})
                yield request

    def artwork_page(self, response):
            dielo = Dielo()

            dielo['id_aukcie']=str(response.meta['auction_id'])
            dielo['autor']=str(response.xpath("//div[@id='right']/h2/a/text()").get())
            dielo['nazov']=str(response.xpath("//div[@id='right']/div[@class='wrapper']/h3/a/text()").get())
            dielo['id_diela']=str(hashlib.md5(f"{dielo['autor']}_{dielo['nazov']}".encode('utf-8')).hexdigest())
            dielo['poradove_cislo']=str(response.xpath("//span[@class='serial']/text()").get())
            dielo['vydrazene']=response.xpath("//span[@class='not_auctioned']").get() is None
            dielo['konecna_cena']=response.xpath("//span[@class='price_auctioned']/text()").get()
            dielo['vyvolavacia_cena']=response.xpath("//span[@class='price_starting']/text()").get()
            dielo['rok']=str(response.xpath('//p[@class="row"]/span[@class="label" and normalize-space(text())="Rok:"]/following-sibling::text()').get()).lstrip()
            dielo['technika']=str(response.xpath('//p[@class="row"]/span[@class="label" and normalize-space(text())="Technika:"]/following-sibling::text()').get()).lstrip()
            dielo['typ_diela']=str(response.xpath('//p[@class="row"]/span[@class="label" and normalize-space(text())="Typ diela:"]/following-sibling::text()').get()).lstrip()
            dielo['rozmery']=str(response.xpath('//p[@class="row"]/span[@class="label" and normalize-space(text())="Rozmery:"]/following-sibling::text()').get()).lstrip()
            dielo['url_soga']=response.url
            dielo['url_soga_obrazok']='https://www.soga.sk'+response.xpath('//div[@id="left"]/div/a/@href').get()

            #print(dielo)
            #print(type(dielo).__name__)
            yield dielo
