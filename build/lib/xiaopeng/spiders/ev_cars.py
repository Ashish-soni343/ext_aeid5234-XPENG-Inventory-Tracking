# Importing required libraries here
import scrapy
import json
import datetime
from os import environ
from ..items import XiaopengItem


# Here spider named "EvCarsSpider" is created
class EvCarsSpider(scrapy.Spider):
    name = 'ev_cars'


    # Here allowed domain and start url of the all 4 car models website are defined that we are crawling
    allowed_domains = ['http://store.xiaopeng.com/']
    start_urls = ['https://store.xiaopeng.com/configurate.html?carSeries=P7&entry=12_1_2#/P7/step1', "https://store.xiaopeng.com/configurate.html?carSeries=P5&entry=12_1_2#/P5/step1", "https://store.xiaopeng.com/configurate.html?carSeries=G3i&entry=12_1_2#/G3i/step1", "https://store.xiaopeng.com/configurate.html?carSeries=G9&entry=12_1_2#/G9/step1"]


    # Here all Mandatory Fields Data are defined under main class that will be called using "self."
    execution_id = ""                                       # This is taken automatically from zyte in further code
    feed_code = "aeid5234"
    record_create_by = "aeid5234_ev_cars"
    record_create_dt = datetime.datetime.utcnow().strftime('%Y-%m-%d %T')
    site = "https://store.xiaopeng.com"
    source_country = "Global"
    src = ""                                                # This is taken dynamically in further code
    type = "XPENG EV CARS"


    # Here we are defining custom settings that are needed for crawling
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 20,
        'DUPEFILTER_DEBUG': True,
    }


    # Here we are defining start_requests function for starting the crawling requests of the urls
    def start_requests(self):
        for start_url in self.start_urls:
            print("start_url===", start_url)
            yield scrapy.Request(url=start_url, callback=self.parse)


    # Here we are defining parse function, inside this function we are writing code for crawling the data
    def parse(self, response):
        items = XiaopengItem()                              # Object to store data in items.py
        data = response.css('script::text').get()           # Here we are fetching script data in which all the website page data is present


        # Here we are Removing extra data coming at front and end of the script
        data = data.replace('window.__INITIAL_STATE__=', "")
        data = data.replace(";", "")


        # Here we are converting the coming script data from string to dictionary using json.loads
        data1 = json.loads(data)
        print("data1====", data1)
        print("data1====", type(data1))


        # Here from this for loop we are fetching all the data that are required from website by going one by one inside dictionaries
        for i in data1['vgroups']:
            # Here we are checking the "carSeriesCode" and proceeding according to that
            if (i['carSeriesCode'] == 'P7') or (i['carSeriesCode'] == 'P5') or (i['carSeriesCode'] == 'G3i') or (i['carSeriesCode'] == 'G9'):

                # Here we are writing condition for "carVersionList" when its is empty
                if len(i['carVersionList']) == 0:
                    # Here we are fetching required data which are available like Model, Inventory, Car series name in this and for other required value which are not present we are passing empty string
                    items["Model"] = i['carYearName']                          # For fetching car model when "carVersionList" is empty
                    items["Car"] = i['carSeriesName']                          # For fetching car series name when "carVersionList" is empty
                    items["Car_Version"] = "null"
                    items["Delivery_time"] = "null"
                    items["Price"] = "null"

                    if i["isSale"] == 0:                                       # For fetching inventory and no inventory data when "carVersionList" is empty
                        items["Inventory"] = "暂无库存"
                    else:
                        items["Inventory"] = "Available"

                    meta = i['tagTitle']                                       # For fetching Metadata when "carVersionList" is empty
                    print("meta===", meta)
                    meta = json.loads(meta)
                    metadata = ""
                    for k in meta:
                        title = k["title"]
                        content = k["content"]
                        if len(metadata) != 0:
                            metadata = metadata + " "
                        metadata = metadata + (title + " " + content)
                    items["Metadata"] = metadata

                    items['Execution_id'] = environ.get('SHUB_JOBKEY', None)
                    items["Feed_code"] = self.feed_code
                    items["Record_create_by"] = self.record_create_by
                    items["Record_create_dt"] = self.record_create_dt
                    items["Site"] = self.site
                    items["Source_country"] = self.source_country
                    items["Src"] = self.src
                    items["Type"] = self.type
                    items["Src"] = response.url
                    yield items                                                 # yielding items here for the condition when "carVersionList" is empty


                # Here we are using for loop for iterating all the required data like cars Model, Car series name, Car versions, Meta data, Price, No inventory, Delivery time
                for j in i['carVersionList']:

                    meta = i['tagTitle']                                        # For fetching Metadata
                    print("meta===", meta)
                    meta = json.loads(meta)
                    metadata = ""
                    for k in meta:
                        title = k["title"]
                        content = k["content"]
                        if len(metadata) != 0:
                            metadata = metadata + " "
                        metadata = metadata + (title + " " + content)
                    items["Metadata"] = metadata

                    items["Model"] = i['carYearName']                           # For fetching car model
                    items["Car"] = j['carSeriesName']                           # For fetching car series name
                    items["Car_Version"] = j['carVersionName']                  # For fetching car version name

                    if j["isSale"] == 0:                                        # For fetching inventory and no inventory data
                        items["Inventory"] = "暂无库存"
                        items["Delivery_time"] = "null"  # For fetching delivery time
                    else:
                        items["Inventory"] = "Available"
                        items["Delivery_time"] = j['expectDeliveryTime']  # For fetching delivery time

                    price_package = j['pricePackage']['personSubsidyAfterSalePrice']        # For fetching price
                    desired_representation_price = "{:,}".format(price_package)             # Formatting price in a required format
                    items["Price"] = "¥" + " " + desired_representation_price


                    # Here we are using storing mandatory data in items.py and some data is taken from self. because we have defined it in the main class
                    items['Execution_id'] = environ.get('SHUB_JOBKEY', None)       # Fetching from zyte using "shub_jobkey"
                    items["Feed_code"] = self.feed_code
                    items["Record_create_by"] = self.record_create_by
                    items["Record_create_dt"] = self.record_create_dt
                    items["Site"] = self.site
                    items["Source_country"] = self.source_country
                    items["Src"] = self.src
                    items["Type"] = self.type
                    items["Src"] = response.url                                     # Fetching from website using "response.url"
                    yield items                                                     # yielding all items here
