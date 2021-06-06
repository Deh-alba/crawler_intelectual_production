# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerIntelectualProductionItem(scrapy.Item):
    # define the fields for your item here like:
    id_status = scrapy.Field()
    title_production = scrapy.Field()
    site_id = scrapy.Field()
    year = scrapy.Field()
    university=scrapy.Field()
    program = scrapy.Field()
    type_production =scrapy.Field()
    sub_type_production =scrapy.Field()
    autors =scrapy.Field()
