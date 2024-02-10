# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SogaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Aukcia(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    nazov = scrapy.Field()
    datum= scrapy.Field()
    popis = scrapy.Field()
    url = scrapy.Field()

class Dielo(scrapy.Item):
    # define the fields for your item here like:
    id_aukcie=scrapy.Field()
    id_diela=scrapy.Field()
    autor = scrapy.Field()
    nazov = scrapy.Field()
    poradove_cislo = scrapy.Field()
    vydrazene=scrapy.Field()
    konecna_cena = scrapy.Field()
    vyvolavacia_cena = scrapy.Field()
    rok=scrapy.Field()
    technika=scrapy.Field()
    typ_diela=scrapy.Field()
    rozmery=scrapy.Field()
    url_soga=scrapy.Field()
    url_soga_obrazok=scrapy.Field()