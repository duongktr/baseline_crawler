import scrapy
from items import ImageDownloadItem
import pandas as pd
from selenium import webdriver

class ImageSpider(scrapy.Spider):

    name = 'ImageSpider'

    #file urls.csv include 'url' column containing url, 'domain' column containing domain
    #read csv file to dataframe
    df = pd.read_csv('urls.csv', usecols=['url', 'domain']).dropna().reset_index()

    def __init__(self, name=None, **kwargs):
        super(ImageSpider, self).__init__(name, **kwargs)
        #read dataframe to list urls
        self.start_urls = self.df['url'].values.tolist() 
        #read dataframe to list domains
        self.allowed_domains = self.df['domain'].values.tolist()

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
        
        #get url image in flickr website
        for photo in response.css('img'):
            photo_url = format_url(photo.attrib["src"])
            yield scrapy.Request(photo_url, self.parse_image)

        driver.quit()
   
    def parse_image(self, response):
        return ImageDownloadItem(url=response.photo_url)
        

#format url for flickr
def photo_url_flickr(photo):
    return 'https://live.staticflickr.com/{server}/{id}_{secret}_{size}.jpg'.format(
        server=photo.xpath('@server').extract_first(),
        id=photo.xpath('@id').extract_first(),
        secret=photo.xpath('@secret').extract_first(),
        size='b',
    )

#format
def format_url(url):
    return 'https:'+url
