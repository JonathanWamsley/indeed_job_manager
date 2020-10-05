import webbrowser
import datetime
from typing import List, Dict
from process_jobs import process_jobs, load_database_jobs, write_file
from job_applier.scraper import Scraper
#from IPython.display import clear_output

class JobManager:
    '''The job manager gets and processes new jobs, applies to jobs, and keeps track of jobs'''
    
    MENU_PROMPT = '''
    Main Menu: type 
        "scrape" to scrape new jobs,
        "apply"  to apply to new jobs,
        "quit"   to quit
        :'''
    
    APPLY_PROMPT = '''
    Application Menu: type
        "commit all"  to commit all,
        "commit # #"  to commit only those #,
        "commit none" to commit none,
        "quit" to go to main menu
        :'''
    
    def __init__(self, title_keywords: List[str], must_have_keyword_groups: List[List[str]], nice_to_have_keywords: [List], indeed_starting_urls: List[str], job_tab_amount: int, resume: str):
        self.title_keywords = title_keywords
        self.must_have_keyword_groups = must_have_keyword_groups
        self.nice_to_have_keywords = nice_to_have_keywords
        self.indeed_starting_urls = indeed_starting_urls
        self.job_tab_amount = job_tab_amount 
        self.resume = resume
        
        self.throw_error_if_scrape__more_than_once = False


    def __str__(self):
        return f'''
        users job information: 
            title keywords: {self.title_keywords}, 
            must have keyword groups: {self.must_have_keyword_groups}, 
            nice to have keywords: {self.nice_to_have_keywords}, 
            starting urls: {self.indeed_starting_urls}, 
            job tab amount: {self.job_tab_amount}, 
            resume version: {self.resume}
            '''
    
    def __repr__(self):
        return f'''
            <JobManager(
            {self.title_keywords}, 
            {self.must_have_keyword_groups}, 
            {self.nice_to_have_keywords}, 
            {self.indeed_starting_urls}, 
            {self.job_tab_amount}, 
            {self.resume}
            )>'''
        
    def start(self) -> None:
        '''executes the user interface for the job manager'''
        selection = input(JobManager.MENU_PROMPT)
        while selection != 'quit':
            if selection == 'scrape':
                self.webscrape_jobs()
            elif selection == 'apply':
                jobs_db = load_database_jobs()
                new_jobs = self.get_new_jobs(jobs_db)
                total_jobs_left = len(new_jobs)
                print(f'there are currently {len(new_jobs)} jobs')
                for index in range(0, len(new_jobs), self.job_tab_amount):      
                    current_jobs = self.get_current_jobs(new_jobs, index)
                    self.open_job_urls(current_jobs)
                    self.print_job_info(current_jobs, total_jobs_left)
                    selection_2 = input(JobManager.APPLY_PROMPT)
                    while not self.is_valid_amount(selection_2, current_jobs):
                        selection_2 = input(JobManager.APPLY_PROMPT)
                    if selection_2 == 'quit':
                        break
                    selected_index = self.parse_input(selection_2, current_jobs)
                    self.commit_jobs(selected_index, current_jobs, jobs_db)
            elif selection == 'quit':
                break
            selection = input(JobManager.MENU_PROMPT)

    def webscrape_jobs(self) -> None:
        '''web scrapes jobs, process them by keywords, then stores them in db'''
        if self.throw_error_if_scrape__more_than_once == False:
            self.throw_error_if_scrape__more_than_once = True
            print('scraping jobs... This may take some time...')
            scraper = Scraper()
            scraper.run_spiders(self.indeed_starting_urls)
            process_jobs(self.title_keywords, self.must_have_keyword_groups, self.nice_to_have_keywords)
            # clear_output(wait=False) # jupyter notebook print supression
        else:
            # Solution to run scraper many times can be found,
            # but not worth the trouble as of now
            # https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable
            print('Sorry, the script/kernal must be reset to scrape again')

    def get_new_jobs(self, jobs_db: List[Dict]) -> List[Dict]:
        '''gets jobs user is intersted in that is sorted by most recent, and amount of keywords'''
        filtered_jobs = [job for job in jobs_db if job['interested'] == True and job['applied_to'] == False]
        sorted_jobs = sorted(filtered_jobs, key = lambda x: (x['scraped_on'], len(x['nice_keywords'])), reverse = True)
        return sorted_jobs

    def get_current_jobs(self, new_jobs: List[Dict], index: int) -> List[Dict]:
        '''gets jobs from a list at JOB_TAB_AMOUNT at a time'''
        if index + self.job_tab_amount <= len(new_jobs):
            return new_jobs[index:index+self.job_tab_amount]
        else:
            return new_jobs[index:]

    def open_job_urls(self, jobs: List[Dict]) -> None:
        '''opens jobs in new tabs'''
        print('\n---Found job links---')
        for job in jobs:
            url = job['url']
            print(url)
            webbrowser.open_new_tab(url)
        print()

    def print_job_info(self, jobs: List[Dict], total_jobs_left: int) -> None:
        '''pretty print showing user job number reference and nice job details to know'''
        print(f'There are {total_jobs_left} left')
        total_jobs_left -= len(jobs)
        for idx, job in enumerate(jobs):
            print(f'{idx}. {job["title"]}: {job["nice_keywords"]}')

    def is_valid_amount(self, user_input: str, current_jobs: List[Dict]) -> bool:
        '''makes sure input is valid a string and numbers are valid if present'''
        if not user_input:
            return False
        return self.valid_string(user_input) or self.valid_numbers(user_input, current_jobs)
            
    def valid_string(self, user_input: str) -> bool:
        '''True if any application condition is found'''
        stopping_conditions = ['commit all', 'commit none', 'quit']
        return any([user_input == condition for condition in stopping_conditions])    
    
    def valid_numbers(self, user_input: str, current_jobs: List[Dict]) -> bool:
        '''checks to see if commit numbers are valid'''
        # test case where there are not a full page of job fails unless commit #
        user_input = user_input.split()
        if user_input[0] != 'commit':
            return False
        if not all([value.isnumeric() for value in user_input[1:]]):
            return False
        if all([0 <= int(value) < len(current_jobs) for value in user_input[1:]]):
            return True
        return False

    def parse_input(self, user_input: str, current_jobs: List[Dict]) -> List[int]:
        '''transforms commit into list of numbers'''
        if user_input == 'commit all':
            return list(range(len(current_jobs)))
        elif user_input == 'commit none':
            empty_list: List[int] = []
            return empty_list
        elif self.valid_numbers(user_input, current_jobs):
            user_input = user_input.split()
            return [int(value) for value in user_input[1:]]
        else:
            raise ValueError("input was not valid")

    def commit_jobs(self, applied_to_list: List[int], applied_to_jobs: List[Dict], jobs_db: List[Dict]) -> None:
        '''filters out which jobs the user was interested then updates db'''
        for idx, job in enumerate(applied_to_jobs):
            if idx in applied_to_list:
                self.register_job(job, jobs_db)
            else:
                self.register_not_interested(job, jobs_db)
        database_jobs_path = 'database_jobs.json'
        write_file(database_jobs_path, jobs_db)

    def register_job(self, current_job: Dict, jobs_db: List[Dict]) -> None:
        '''user successfully applied to job'''
        jobs_id = current_job['info']
        for job in reversed(jobs_db):
            if jobs_id in job['info']:
                job['applied_to'] = True
                job['applied_on'] = str(datetime.date.today())
                job['resume_sent'] = self.resume

    def register_not_interested(self, current_jobs: Dict, jobs_db: List[Dict]) -> None:
        '''keeps track of jobs that should have been applied to but were not'''
        jobs_id = current_jobs['info']
        for job in reversed(jobs_db):
            if jobs_id in job['info']:
                job['interested'] = False
                job['false positive'] = True
