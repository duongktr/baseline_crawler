import scrapy
from items import ImageDownloadItem
import os
from selenium import webdriver

class ImageSpider(scrapy.Spider):

    name = 'ImageSpider'

    def __init__(self, name=None, **kwargs):
        super(ImageSpider, self).__init__(name, **kwargs)
        self.start_urls = ['https://www.flickr.com/photos/ryanlenguyen'] #example: url get image
        self.allowed_domains = ['www.flickr.com']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        #config selenium chrome
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        #scroll to the end of page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #prevent lazy loading
        
        #get url image
        for photo in response.css('img').getall():
            photo_url = format_url(photo.attrib["src"])
            yield {
                "url": photo_url
            }
        driver.quit()
    
    def parse_images(self, response):
        item = ImageDownloadItem()
        yield item
        

def photo_url_flickr(photo):
    return 'https://live.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
        server=photo.xpath('@server').extract_first(),
        id=photo.xpath('@id').extract_first(),
        secret=photo.xpath('@secret').extract_first(),
        size='b',
    )

def format_url(url):
    return 'https:'+url
