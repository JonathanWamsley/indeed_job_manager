from job_manager import JobManager

# jobs must contain one of these titles
TITLE_KEYWORDS = ['engineer', 'software-engineer', 'dataengineer', 'data-engineer', 'data']

# jobs must contain one group keyword in job description for every group
MUST_HAVE_KEYWORD_GROUPS = [['python', 'python3']]

# job will update all nice to have keywords founds
NICE_TO_HAVE_KEYWORDS = ['pandas', 'webscraping', 'dash', 'scrapy', 'etl', 'pipeline']

# Starting urls from indeed site, can add job titles, experience level, etc
INDEED_STARTING_URLS = [
        "https://www.indeed.com/jobs?q=data+engineer&jt=fulltime&explvl=entry_level",
        "https://www.indeed.com/jobs?q=software+engineer&jt=fulltime&explvl=entry_level",
    ]

# amount of jobs opening at a time
JOB_TAB_AMOUNT = 5

# resume you are sending out
RESUME = 'V1.00'


if __name__ == '__main__':
    user = JobManager(TITLE_KEYWORDS, 
                      MUST_HAVE_KEYWORD_GROUPS,
                      NICE_TO_HAVE_KEYWORDS,
                      INDEED_STARTING_URLS,
                      JOB_TAB_AMOUNT,
                      RESUME)
    print(user)
    user.start()
    