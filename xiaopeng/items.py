# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaopengItem(scrapy.Item):
    # define the fields for your item here like:
    Model = scrapy.Field()
    Car = scrapy.Field()
    Car_Version = scrapy.Field()
    Inventory = scrapy.Field()
    Delivery_time = scrapy.Field()
    Price = scrapy.Field()
    Metadata = scrapy.Field()
    Execution_id = scrapy.Field()
    Feed_code = scrapy.Field()
    Record_create_by = scrapy.Field()
    Record_create_dt = scrapy.Field()
    Site = scrapy.Field()
    Source_country = scrapy.Field()
    Src = scrapy.Field()
    Type = scrapy.Field()
    Src = scrapy.Field()
    pass
