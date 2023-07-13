# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from pprint import pformat

class ImageDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    url = Field()
    author = Field()
    size = Field()

    def __str__(self) -> str:
        return pformat({
            'image_url': self['url'],
            'image_author': self['author'],
            'size': self['size']
        })