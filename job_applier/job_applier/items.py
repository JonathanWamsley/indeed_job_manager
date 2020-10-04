import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags


def filter_ad(values):
    if "Responded" in values:
        loc = values.find("Responded")
        return values[:loc]

    if "reviewsRead" in values:
        loc = values.find("reviewsRead")
        return values[:loc]
    return values

def is_easy_apply(values=False):
    return True if values else False


class IndeedWebscraperItem(scrapy.Item):
    
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    info = scrapy.Field(
        input_processor=MapCompose(remove_tags, filter_ad),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst(),
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    easy_apply = scrapy.Field(
        output_processor=TakeFirst()
    )
    scraped_on = scrapy.Field(
        output_processor=TakeFirst()
    )