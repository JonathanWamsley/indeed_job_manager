import scrapy
from scrapy.loader import ItemLoader
from job_applier.job_applier.items import IndeedWebscraperItem
import datetime


class IndeedSpider(scrapy.Spider):
    name = "indeed"

    def __init__(self, urls=["https://www.indeed.com/jobs?q=data+engineer&jt=fulltime&explvl=entry_level"], **kwargs):
        self.start_urls = urls
        super().__init__(**kwargs)

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        jobs = response.xpath("//h2[@class='title']/a")
        for job in jobs:
            url_path = job.xpath('.//@href').get()
            url_link = response.urljoin(url_path)
            yield scrapy.Request(url=url_link, callback=self.parse_items)

        next_page = response.xpath("//div[@class='pagination']/ul/li/a[@aria-label='Next']").get()
        if next_page:
            next = response.xpath("//div[@class='pagination']/ul/li/a/@href")[-1].get()
            next_url = response.urljoin(next)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_items(self, response):
        loader = ItemLoader(IndeedWebscraperItem(), response)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('info', "//*[contains(@class,'jobsearch-DesktopStickyContainer')]")
        loader.add_xpath('description', "//div[@id = 'jobDescriptionText']")
        loader.add_value('url', response.request.url)
        easy_apply_button =  response.xpath("//div[@class = 'jobsearch-IndeedApplyButton-contentWrapper']").get()
        easy_apply = True if easy_apply_button else False
        loader.add_value('easy_apply', easy_apply)
        loader.add_value('scraped_on', datetime.date.today())
        yield loader.load_item()
