# Python 3 script to make an API call to get a list of courses from
# an account and write results to CSV file. The account provisioning report
# provides more data but this can serve as the foundation for other API work.

import requests # requests module must be installed in python environment
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files

os.system('cls' if os.name == 'nt' else 'clear') # clears screen

# variables for Canvas instance and to define account
account_url = '<INSERT INSTANCE URL>'
token = '<INSERT TOKEN>'
header = {'Authorization': 'Bearer ' + '%s' % token}
account = '<INSERT ROOT ACCOUNT ID>' # parent account from which to generate list

# List of coures from specific account
def get_Courses(Account_ID):
    print ('Initiating request...')

    # Open CSV
    f = open('course_list.csv', 'a')
    f.write('%s, %s, %s, %s, %s, %s \n' % ('SIS ID', 'Canvas ID',
        'Course Name', 'Account ID', 'Public', 'Term'))

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
            id = str(i.get('id'))
            account_id = str(i.get('account_id'))
            is_public = str(i.get('is_public'))
            sis_course_id = str(i.get('sis_course_id'))
            course_name = i.get('name').replace(',', ' ')
            term = i.get('enrollment_term_id')
            f.write('%s, %s, %s, %s, %s, %s \n' %
                (sis_course_id, id, course_name, account_id, is_public, term))

        if len(response) == 100:
            print('Processing results:', (page_no * 100))
            page_no +=1 # if 100 items returned more pages remaining
        elif len(response) < 100: # final page
            loop_control = 1;

    # Close CSV
    f.close

get_Courses(account)
