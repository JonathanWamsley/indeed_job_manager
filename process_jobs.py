import json
import os

### get new jobs
def get_new_jobs():
    '''returns the never before seen jobs from the webscraped jobs'''
    new_jobs_path = 'new_jobs.json'
    new_jobs = read_file(new_jobs_path)
    
    database_jobs = load_database_jobs()
    new_jobs = filter_duplicate_jobs(new_jobs, database_jobs)
    return new_jobs

def filter_duplicate_jobs(new_jobs, old_jobs):
    '''returns unique jobs in the new jobs list'''   
    unique_job_id = {old_job['info']:True for old_job in old_jobs}
    unique_jobs = [new_job for new_job in new_jobs if new_job['info'] not in unique_job_id]
    return unique_jobs

### label jobs
def filter_title_keywords(title_keywords, job):
    '''check if any title keywords contain an exact match to a job title'''
    return any(title in set(job['title'].lower().split()) for title in title_keywords)

def filter_must_have_keywords(must_have_keywords, job):
    '''asserts that all must have keyword groups contain at least one instance in the description'''
    description = ((job['description'].lower().replace('\n', ' ')).split())
    for keyword_group in must_have_keywords:
        if not any([keyword in description for keyword in keyword_group]):
            return False
    return True

def filter_job_by_keywords(titles_keywords, must_have_keywords, job):
    '''returns True if the job pass the title and must have keyword filters'''
    return filter_title_keywords(titles_keywords, job) and filter_must_have_keywords(must_have_keywords, job)

def filter_nice_to_have_keywords(nice_to_have_keywords, job):
    '''return found nice to have keywords if the job page'''
    description = ((job['description'].lower().replace('\n', ' ')).split())
    found_nice_to_have_keywords = []
    for nice_to_have_keyword in nice_to_have_keywords:
        if nice_to_have_keyword in description:
            found_nice_to_have_keywords.append(nice_to_have_keyword)
    return found_nice_to_have_keywords
    
def label_jobs(titles_keywords, must_have_keywords, nice_to_have_keywords, jobs):
    '''labels jobs by keyword interest'''
    for job in jobs:
        job['interested'] = filter_job_by_keywords(titles_keywords, must_have_keywords, job)
        job['nice_keywords'] = filter_nice_to_have_keywords(nice_to_have_keywords, job)         
        job['applied_to'] = False
        job['applied_on'] = None
        job['resume_sent'] = None

    return jobs

### update database
def add_new_jobs_to_database(new_jobs):
    database_jobs_path = 'database_jobs.json'
    update_file(database_jobs_path, new_jobs)
    
### utilities
def load_database_jobs():
    database_jobs_path = 'database_jobs.json'
    if os.path.exists(database_jobs_path) == False:
        write_file(database_jobs_path, [])
    database_jobs = read_file(database_jobs_path)
    return database_jobs

def read_file(path):
    with open(path, 'rb') as f:
        data = json.load(f)
    return data

def write_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)
        
def update_file(path, data):
    existing_data = read_file(path)
    existing_data.extend(data)
    write_file(path, existing_data)

### main caller
def process_jobs(title_keywords, must_have_keywords, nice_to_have_keywords):
    '''gets the never before seen jobs, filters them by keywords, labels them and updates them in the database'''
    new_jobs = get_new_jobs()
    labeled_jobs = label_jobs(title_keywords, must_have_keywords, nice_to_have_keywords, new_jobs)
    add_new_jobs_to_database(labeled_jobs)
