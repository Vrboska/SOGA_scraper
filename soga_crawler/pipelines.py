# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from logging import log
from sqlite3 import dbapi2 as sqlite

class SogaCrawlerPipeline:
    def process_item(self, item, spider):
        return item
    
    
class AuctionPipeline(object):
    def __init__(self):
        # Possible we should be doing this in spider_open instead, but okay
        self.connection = sqlite.connect('./soga.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS aukcie')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS aukcie'\
                    '(id VARCHAR(256) PRIMARY KEY, nazov VARCHAR(256), popis VARCHAR(256)'\
                    ',url VARCHAR(256))')

    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        self.cursor.execute("select * from auctions where id=?", (item['id'],))
        result = self.cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
        else:
            self.cursor.execute(
                "insert into aukcie (id, nazov, popis, url) values (?, ?, ?, ?)",
                    (item['id'], item['nazov'], item['popis'], item['url']))

            self.connection.commit()

            #log.msg("Item stored : " % item, level=log.DEBUG)
        return item

    def handle_error(self, e):
        log.err(e)

class DieloPipeline(object):
    def __init__(self):
        # Possible we should be doing this in spider_open instead, but okay
        self.connection = sqlite.connect('./soga.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS diela')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS diela'\
                    '(id_aukcie VARCHAR(256), id_diela VARCHAR(256), autor VARCHAR(256)'\
                    ',nazov VARCHAR(256), poradove_cislo VARCHAR(256), vydrazene VARCHAR(256)'\
                    ',konecna_cena  VARCHAR(256), vyvolavacia_cena VARCHAR(256), rok VARCHAR(256)'\
                    ',technika  VARCHAR(256), typ_diela VARCHAR(256), rozmery VARCHAR(256)'\
                    ',url_soga  VARCHAR(256), url_soga_obrazok VARCHAR(256))'\
                            )

    # Take the item and put it in database - do not allow duplicates
    def process_item(self, item, spider):
        self.cursor.execute("select * from diela where id_aukcie=? and id_diela=?", (item['id_aukcie'],item['id_diela']))
        result = self.cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
        else:
            self.cursor.execute(
                "insert into aukcie (id_aukcie, id_diela, autor, nazov, poradove_cislo, vydrazene,konecna_cena,vyvolavacia_cena,rok,technika,typ_diela,rozmery,url_soga, url_soga_obrazok) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (item['id_aukcie'], item['id_diela'], item['autor'], item['nazov'], item['poradove_cislo'], item['vydrazene'], item['konecna_cena'], item['vyvolavacia_cena'], item['rok'], item['technika'], item['typ_diela'], item['rozmery'], item['url_soga'], item['url_soga_obrazok']))

            self.connection.commit()

            log.msg("Item stored : " % item, level=log.DEBUG)
        return item

    def handle_error(self, e):
        log.err(e)