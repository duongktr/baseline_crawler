# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

class ImageDownloadPipeline:
    def process_item(self, item, spider):
        output_dir = 'data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = item['url'].split('/')[-1]
        with open(os.path.join(output_dir, filename), 'wb') as f:
            f.write(item['url'])
        return item
