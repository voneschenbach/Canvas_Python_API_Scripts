# Python 3 script create a CSV of course-level LTIs

import requests # requests module must be installed in python environment
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files

os.system('cls' if os.name == 'nt' else 'clear') # clears screen

# variables for Canvas instance and to define account
account_url = '<INSERT INSTANCE URL HERE>'
token = '<INSERT KEY HERE>'
header = {'Authorization': 'Bearer ' + '%s' % token}
account = '<INSERT ROOT ACCOUNT HERE>' # parent account from which to generate list


# List of coures from one account
def get_Courses(Account_ID):
    print ('Initiating course list process...')
    request_parameters = {} # parameters for filtering, etc.
    page_no = 1  # page number control variable
    loop_control = 0 # while loop control variable
    while loop_control == 0:
        # Get list of courses, 100 courses per page.
        request = requests.get(account_url +
            '/accounts/' + str(Account_ID) + '/courses?per_page=100&page=' +
            str(page_no), params = request_parameters, headers = header)
        response = request.json()
        for i in response:
            listCourseLTI(i.get('id'))
        if len(response) == 100:
            page_no +=1 # if 100 items returned more pages remaining
        elif len(response) < 100: # final page
            loop_control = 1;


# Find installed LTIs for each course by ID
def listCourseLTI(course_id):
    print ('Recording LTIs installed for', course_id)
    LTIs = [] # List to hold the requested data
    request_parameters = {} # Parameters
    # Get list of LTIs installed
    request = requests.get(account_url +
        'courses/' + str(course_id) + '/external_tools',
            params = request_parameters, headers = header)
    response = request.json()

    # Record data in CSV
    f = open('LTI_list.csv', 'a')
    for i in response:
        LTIs.append(i) # append the course JSON object to the list
    json_str = json.dumps(LTIs)
    data = json.loads(json_str)

    for item in data:
        LTI_id = str(item.get('id'))
        LTI_URL = str(item.get('url'))
        LTI_name = str(item.get('name'))
        LTI_created_date = str(item.get('created_at'))
        print(LTI_id, course_id, LTI_URL, LTI_name, LTI_created_date)
        f.write('%s, %s, %s, %s, %s \n' %
            (LTI_id, course_id, LTI_URL, LTI_name, LTI_created_date))

get_Courses(account)
