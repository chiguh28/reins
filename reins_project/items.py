# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReinsProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()
    transaction_mode = scrapy.Field()
    trading_conditions = scrapy.Field()
    property_event = scrapy.Field()
    price = scrapy.Field()
    use_area = scrapy.Field()
    building_coverage_ratio = scrapy.Field()
    floor_area_ratio = scrapy.Field()
    area_square = scrapy.Field()
    area_unit_price = scrapy.Field()
    tsubo_unit_price = scrapy.Field()
    tsubo_unit_price_num = scrapy.Field()
    roadside_situation = scrapy.Field()
    road = scrapy.Field()
    address = scrapy.Field()
    stations_along_the_line = scrapy.Field()
    trade_name = scrapy.Field()
    phone_number = scrapy.Field()
    access = scrapy.Field()
