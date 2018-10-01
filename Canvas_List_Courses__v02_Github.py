# Python 3 script to make an API call to get a list of courses from
# an account and write results to CSV file

import requests # requests module must be installed in python environment
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files

os.system('cls' if os.name == 'nt' else 'clear') # clears screen

# variables for Canvas instance and to define account
account_url = '<INSERT INSTANCE URL>'
token = '<INSERT TOKEN HERE>'
header = {'Authorization': 'Bearer ' + '%s' % token}
account = '<INSERT ACCOUNT>' # parent account from which to generate list

# List of coures from specific account
def get_Courses(Account_ID):
    print ('Initiating request...')
    courses = [] # initialize a list to hold the requested data
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
            courses.append(i) # append the course JSON object to the list
        if len(response) == 100:
            page_no +=1 # if 100 items returned more pages remaining
        elif len(response) < 100: # final page
            loop_control = 1;

        printResults(courses)

# Parse JSON response
def printResults(data):

    json_str = json.dumps(data)
    data = json.loads(json_str)

    # iterates through response and processes data
    results_counter = 0
    f = open('course_list.csv', 'w')
    f.write('%s, %s, %s, %s \n' % ('SIS ID',
        'Course Name', 'Account ID', 'Public'))
    for item in data:
        results_counter += 1 # iterate for each row in the list

        account_id = str(item.get('account_id'))
        is_public = str(item.get('is_public'))
        sis_course_id = str(item.get('sis_course_id'))
        course_name = item.get('name')

        if account_id == account:
            print (sis_course_id, course_name, account_id, is_public)
            f.write('%s, %s, %s, %s \n' %
                (sis_course_id, course_name, account_id, is_public))
    f.close
    print ('Total results:', results_counter)

get_Courses(account)
