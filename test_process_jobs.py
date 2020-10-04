import unittest
from process_jobs import *


class TestProcessJobs(unittest.TestCase):
    
    def setUp(self):
        self.title_keywords = ['engineer', 'dataengineer']
        self.must_have_keyword_groups = [
            ['python', 'python3'],
            ['engineer', 'dataengineer', 'dataengineering', 'data-engineer'],
            ]
        self.nice_to_have_keywords = ['webscraping', 'pandas']
        self.database_jobs = [
            {
                'title': 'Data Engineer duplicate A pass',
                'info': 'Data Engineer duplicate A pass',
                'description': 'Python engineer pass',
                'interested': True,
                'nice_keywords': [],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {
                'title': 'Data Engineer B pass',
                'info': 'Data Engineer B pass',
                'description': 'None fail',
                'interested': False,
                'nice_keywords': [],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
        ]
        self.new_jobs = [
            {
                'title': 'Data Engineer duplicate A pass',
                'info': 'Data Engineer duplicate A pass',
                'description': 'Python engineer pass',
            },
            {
                'title': 'Data Engineer C pass',
                'info': 'Data Engineer C pass',
                'description': 'Python engineer webscraping pass',
            },
            {
                'title': 'title D fail',
                'info': 'title D fail',
                'description': 'Python engineer pandas pass',
            },
            {
                'title': 'Engineer E pass',
                'info': 'Engineer E pass',
                'description': 'description fail',
            },
        ]
        
        self.new_jobs_unique = [
            {
                'title': 'Data Engineer C pass',
                'info': 'Data Engineer C pass',
                'description': 'Python engineer webscraping pass',
            },
            {
                'title': 'title D fail',
                'info': 'title D fail',
                'description': 'Python engineer pandas pass',
            },
            {
                'title': 'Engineer E pass',
                'info': 'Engineer E pass',
                'description': 'description fail',
            },
        ]
        self.new_jobs_labeled = [
            {
                'title': 'Data Engineer C pass',
                'info': 'Data Engineer C pass',
                'description': 'Python engineer webscraping pass',
                'interested': True,
                'nice_keywords': ['webscraping'],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {
                'title': 'title D fail',
                'info': 'title D fail',
                'description': 'Python engineer pandas pass',
                'interested': False,
                'nice_keywords': ['pandas'],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {
                'title': 'Engineer E pass',
                'info': 'Engineer E pass',
                'description': 'description fail',
                'interested': False,
                'nice_keywords': [],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
        ]
        self.database_jobs_updated = [
            {
                'title': 'Data Engineer duplicate A pass',
                'info': 'Data Engineer duplicate A pass',
                'description': 'Python engineer pass',
                'interested': True,
                'nice_keywords': [],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {
                'title': 'Data Engineer B pass',
                'info': 'Data Engineer B pass',
                'description': 'None fail',
                'interested': False,
                'nice_keywords': [],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {   
                'title': 'Data Engineer C pass',
                'info': 'Data Engineer C pass',
                'description': 'Python engineer webscraping pass',
                'interested': True,
                'nice_keywords': ['webscraping'],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {
                'title': 'title D fail',
                'info': 'title D fail',
                'description': 'Python engineer pandas pass',
                'interested': False,
                'nice_keywords': ['pandas'],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
            {
                'title': 'Engineer E pass',                
                'info': 'Engineer E pass',
                'description': 'description fail',
                'interested': False,
                'nice_keywords': [],
                'applied_to': False,
                'applied_on': None,
                'resume_sent': None,
            },
        ]
        
    def tearDown(self):
        pass
    
    def test_filter_duplicate_jobs(self):
        self.assertListEqual(filter_duplicate_jobs(self.new_jobs, self.database_jobs), self.new_jobs_unique)
        
    def test_filter_title_keywords(self):
        self.assertEqual(filter_title_keywords(self.title_keywords, self.new_jobs_unique[0]), True)
        self.assertEqual(filter_title_keywords(self.title_keywords, self.new_jobs_unique[1]), False)
        self.assertEqual(filter_title_keywords(self.title_keywords, self.new_jobs_unique[2]), True)
                         
    def test_filter_must_have_keywords(self):
        self.assertEqual(filter_must_have_keywords(self.must_have_keyword_groups, self.new_jobs_unique[0]), True)
        self.assertEqual(filter_must_have_keywords(self.must_have_keyword_groups, self.new_jobs_unique[1]), True)
        self.assertEqual(filter_must_have_keywords(self.must_have_keyword_groups, self.new_jobs_unique[2]), False)
        
    def test_filter_job_by_keywords(self):
        self.assertEqual(filter_job_by_keywords(self.title_keywords, self.must_have_keyword_groups, self.new_jobs_unique[0]), True)
        self.assertEqual(filter_job_by_keywords(self.title_keywords, self.must_have_keyword_groups, self.new_jobs_unique[1]), False)
        self.assertEqual(filter_job_by_keywords(self.title_keywords, self.must_have_keyword_groups, self.new_jobs_unique[2]), False)
        
    def test_filter_nice_to_have_keywords(self):
        self.assertListEqual(filter_nice_to_have_keywords(self.nice_to_have_keywords, self.new_jobs_unique[0]), ['webscraping'])
        self.assertListEqual(filter_nice_to_have_keywords(self.nice_to_have_keywords, self.new_jobs_unique[1]), ['pandas'])
        self.assertListEqual(filter_nice_to_have_keywords(self.nice_to_have_keywords, self.new_jobs_unique[2]), [])

    def test_label_jobs(self):
        self.assertListEqual(label_jobs(self.title_keywords, self.must_have_keyword_groups, self.nice_to_have_keywords, self.new_jobs_unique), self.new_jobs_labeled)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)