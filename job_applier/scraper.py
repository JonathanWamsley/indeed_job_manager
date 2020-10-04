from job_applier.job_applier.spiders.indeed_spider import IndeedSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class Scraper:
    def __init__(self):
        settings_file_path = 'job_applier.job_applier.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = IndeedSpider # The spider you want to crawl

    def run_spiders(self, urls):
        self.process.crawl(self.spider, urls)
        self.process.start()  # the script will block here until the crawling is finished

# scraper = Scraper()
# scraper.run_spiders()