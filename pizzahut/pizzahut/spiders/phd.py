# -*- coding: utf-8 -*-
import csv

import scrapy
from scrapy.http import FormRequest
from pizzahut.items import PizzahutItem

class PhdSpider(scrapy.Spider):
    name = "phd"
    allowed_domains = ["https://order.phd.co.id"]
    
    def __init__(self, filename=None):
        if filename:
            self.lat_long_data = [i.strip() for i in open(filename).readlines() if i.strip()]

    def start_requests(self):
        POST_DATA = {
                    "limit":"99999999",
                    "start":"0",
                    "gpsLat":"",
                    "gpsLong":""
                    }

        for ll in self.lat_long_data:
            latitude, longitude = ll.split("::")
            POST_DATA["gpsLat"] = str(latitude)
            POST_DATA["gpsLong"] = str(longitude)

            yield FormRequest("https://order.phd.co.id/en/frontend/pizza/getListOutlet", callback=self.parse, \
                    formdata=POST_DATA, dont_filter=True)

    def parse(self, response):
        response_data = response.body
        response_data = response_data.replace('true', '"true"')
        response_data = eval(response_data)

        outlets = response_data["data"]["outlet"]["items"]
        if outlets:
            oitem = PizzahutItem()

            for outlet in outlets:
                oitem["OutletID"] = outlet["OutletID"]
                oitem["OutletName"] = outlet["OutletName"]
                oitem["Description"] = outlet["Description"]
                oitem["OpeningHours"] = outlet["OpeningHours"]
                oitem["Location"] = outlet["Location"]
                oitem["ImageSource"] = outlet["ImageSource"]
                oitem["Latitude"] = outlet["Lat"]
                oitem["Longitude"] = outlet["Long"]
                oitem["ContactNumber"] = outlet["ContactNumber"]

                yield oitem
