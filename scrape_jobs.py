import sys 
from job_applier.scraper import Scraper


if len(sys.argv) > 1:
    start_urls = sys.argv[1:]
    print(start_urls)
else:
    start_urls = [
        "https://www.indeed.com/jobs?q=data+engineer&jt=fulltime&explvl=entry_level",
        "https://www.indeed.com/jobs?q=software+engineer&jt=fulltime&explvl=entry_level",
    ]
scraper = Scraper()
scraper.run_spiders(start_urls)
