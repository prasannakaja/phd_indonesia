# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class PizzahutItem(scrapy.Item):
    # define the fields for your item here like:
    OutletID = scrapy.Field()
    OutletName = scrapy.Field()
    Description = scrapy.Field()
    OpeningHours = scrapy.Field()
    Location = scrapy.Field()
    ImageSource = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    ContactNumber = scrapy.Field()
