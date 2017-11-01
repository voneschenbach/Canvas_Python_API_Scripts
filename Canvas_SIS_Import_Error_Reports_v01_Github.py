# SIS_Import_Status_v01.py
# Python 3 script to view SIS import errors for a given period

import requests # needed for API requests; requests module must be installed in python environment
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files
import time # needed for time delays
import urllib # needed for easier file downloads vs requests method
import datetime # needed to nicely format dates

os.system('cls' if os.name == 'nt' else 'clear') # clears screen

# variables for Canvas instance and to define account
instance_url = 'https://seattleu.instructure.com/api/v1/'
token = '<INSERT TOKEN HERE>'
header = {'Authorization': 'Bearer ' + '%s' % token}
account = '<INSERT ACCOUNT>' # account number of root account

# request SIS import status
def sis_import_status(account):
    print ('Initiating request...')
    request_parameters = {'created_since': '2017-10-08T00:00:01Z'}
    request = requests.get(instance_url + 'accounts/' + str(account)
        + '/sis_imports', params = request_parameters, headers = header)
    response = request.json()

    json_str = json.dumps(response)
    data = json.loads(json_str)

    for items in data['sis_imports']:
        if items['progress'] == 100:  # Restricts to completed imports only
            print (
                '\t========== Import Summary ==========\n',
                '\tImport ID: ' + str(items['id']) + '\n',
                '\tImport Started: ' + str(items['started_at']) + '\n',
                '\tAccounts: ' + str(items['data']['counts']['accounts']) + '\n',
                '\tTerms: ' + str(items['data']['counts']['terms']) + '\n',
                '\tCourses: ' + str(items['data']['counts']['courses']) + '\n',
                '\tSections: ' + str(items['data']['counts']['sections']) + '\n',
                '\tCrosslists: ' + str(items['data']['counts']['xlists']) + '\n',
                '\tUsers: ' + str(items['data']['counts']['users']) + '\n',
                '\tEnrollments: ' + str(items['data']['counts']['enrollments']),
                )

            # Obtain additional details when errors occur
            if items['workflow_state'] == 'imported_with_messages':

                request2 = requests.get(instance_url + 'accounts/' + str(account)
                    + '/sis_imports/' + str(items['id']), headers = header)
                response2 = request2.json()

                json_str2 = json.dumps(response2)
                data2 = json.loads(json_str2)

                for key,value in data2.items():
                    if key == 'processing_warnings':
                        print ('\r\tProcessing warnings:')
                        count = 0
                        error_count = len(value) # Calculates length of list
                        while (count < error_count):
                            print (
                                '\t' + value[count][0] + ': ' + value[count][1],
                                )
                            count += 1
                    elif key == 'processing_errors':
                        print ('\r\tProcessing errors:')
                        count = 0
                        error_count = len(value) # Calculates length of list
                        while (count < error_count):
                            print (
                                '\t' + value[count][0] + ': ' + value[count][1],
                                )
                            count += 1
            print ('\t====================================\n\n',)

sis_import_status(account)
