# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonTutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_title = scrapy.Field()
#     product_price = scrapy.Field()
#     product_imageLink = scrapy.Field()
#     product_hyperLink = scrapy.Field()
