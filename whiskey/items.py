# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose#, TakeFirst
from w3lib.html import remove_tags

def remove_front_back_whitespace(value):
    return value.strip()

def remove_currency(value):
    return value.strip().replace('£', '')

'''
    You can import TakeFirst from itemloaders.processors above and use it. The reason why I create another one 
    here is bcus TakeFirst will return the first non-null/non-empty value from the values received. 
    Example:

    >>> from itemloaders.processors import TakeFirst
    >>> proc = TakeFirst()
    >>> proc(['', 'one', 'two', 'three'])
    'one'

    But in my case, I want to export my crawled data to csv or JSON file. So, I want my function to return None 
    while the partiicular data That I scrapped cannot be found (None or ''). Otherwise, the key-value for the 
    particular data will not be created. Example:

    By using the TakeFirst class import from itemloaders.processors,
    >>> Name, Volume and Alcohol_Percent cannot be found during scraping
    >>> [{"Region": "Highland", "Price_Pound": "325.00", "Link": "https://www.whiskyshop.com/aberlour-a-bunadh"}]

    By using the TakeFirst class below (created my own),
    >>> Name, Volume and Alcohol_Percent cannot be found during scraping
    >>> [{"Name": None, "Volume": None, "Alcohol_Percent": None, "Region": "Highland", "Price_Pound": "325.00", "Link": "https://www.whiskyshop.com/aberlour-a-bunadh,Aberlour"}]
'''
class TakeFirst:
    def __call__(self, values):
        for value in values:
            if value is None or value == '':
                return None
            else:
                return value

class WhiskeyItem(scrapy.Item):
    Name = scrapy.Field(input_processor = MapCompose(remove_tags, remove_front_back_whitespace), output_processor = TakeFirst())
    Volume = scrapy.Field(input_processor = MapCompose(remove_tags, remove_front_back_whitespace), output_processor = TakeFirst())
    Alcohol_Percent = scrapy.Field(input_processor = MapCompose(remove_tags, remove_front_back_whitespace), output_processor = TakeFirst())
    Region = scrapy.Field(input_processor = MapCompose(remove_tags, remove_front_back_whitespace), output_processor = TakeFirst())
    Price_Pound = scrapy.Field(input_processor = MapCompose(remove_tags, remove_front_back_whitespace, remove_currency), output_processor = TakeFirst())
    Link = scrapy.Field(output_processor = TakeFirst())
