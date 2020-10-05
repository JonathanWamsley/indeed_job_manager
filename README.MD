# Indeed Job Applier and Manager

- An Python application that helps users:
    1. Find desired jobs from indeed
    2. Quickly apply to interested jobs
    3. Keep track of application history


### Demo

[![https://i9.ytimg.com/vi/l3ZcHgI6aH0/mq1.jpg?sqp=CKzT7fsF&rs=AOn4CLAp7ma_x2GjYZJJmNunXy31R3h4lA](https://img.youtube.com/vi/l3ZcHgI6aH0/0.jpg)](https://www.youtube.com/watch?v=l3ZcHgI6aH0 "Indeed Job Applier and Manager")

### User options

- Users provide:
    - Indeed Starting Urls: list
        - starting url starts from indeed and can contain filters like
            - job title
            - full time/ part time
            - experience level
            - ex: "https://www.indeed.com/jobs?q=data+engineer&jt=fulltime&explvl=entry_level"
    - Title keywords: list
        - jobs must contain one of these key words
    - Must have keywords: list of lists
        - jobs must contain one group of eay keyword in the job description
    - Nice to have keywords: list
        - db registers all the nice to have keywords found in the job description
    - Resume ID: string
        - keep track of what resume was sent to a company
    - Job Tab Amount: int
        - toggle how many pages you want to apply to open and apply to at a time

### Project components

##### Jobs ETL
- scrapes indeed using starting url
- filters jobs by keywords
- labels jobs and stores them into a json database

##### Semi-Automated Job applier
- User gets N desired jobs urls that automatically opens in new tabs
- User can commit which jobs the user applied to
- Job is successfully registered in the database

##### Job Tracker (Not Implemented yet)
- Tracks where and how many jobs have been applied to
- Tracks how many false positives there have been


##### Todo

- add requirements
- add installation guide
- add system and integration tests