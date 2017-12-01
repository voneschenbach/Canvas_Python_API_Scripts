# Python 3 script to make a series of API calls to get a course provisioning
# report from an account, download it, parse it to determine file quotas for
# each user, write that information to a new file.

import requests # needed for API requests
import json # needed to format results for display or export
import os # needed to clear screen for new output each time program run
import csv # needed to read/write csv files
import time # needed for time delays
from urllib.request import urlretrieve # download files
import datetime # needed to nicely format dates

os.system('cls' if os.name == 'nt' else 'clear') # clears screen


# variables for Canvas instance and to define account
instance_url = 'https://seattleu.instructure.com/api/v1/'
token = '<INSERT KEY HERE>'
header = {'Authorization': 'Bearer ' + '%s' % token}
account = '<INSERT ACCOUNT>' # account number from which to generate list



# start a report request for account defined above
def start_report(account):
    print ('Initiating request...')
    request_parameters = {'parameters[users]': True}
    request = requests.post(instance_url + '/accounts/' + str(account)
        + '/reports/provisioning_csv', params = request_parameters,
        headers = header)
    response = request.json()

    # display results of start report request
    json_str = json.dumps(response)
    data = json.loads(json_str)
    status = data['status']
    report_id = data['id']

    # check to see if request was successful
    if status == 'running':
        print ('Report request successful.')
        report_status(report_id)
    else:
        print ('Report request was not successful')


# get status of running report; when ready download file
def report_status(report_id):

    print ('Determining report status for', report_id, '...')
    request = requests.get(instance_url + '/accounts/' + str(account)
        + '/reports/provisioning_csv/', str(report_id), headers = header)
    response = request.json()

    for items in response:
        id = str(items.get('id'))

        if items.get('id') == report_id:
            progress = int(items.get('progress'))

            if progress == 100: # ensures that report is ready
                attachments = items.get('attachment')
                report_url = str(attachments.get('url'))
                print ('Report ID:', id, 'Download URL', report_url)
                download_report(report_url)
            else:
                print ('Report not ready yet. Retrying in 10 seconds...')
                time.sleep(10)
                report_status(report_id)


# download report to current working directory
def download_report(report_url):
    print ('Downloading report...')
    filename = 'Canvas_User_Quota_Report_' + datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
    print ('File name to be written: ' + filename)
    urlretrieve(report_url, filename)
    print ('Report saved successfully.')
    read_users(filename)

# open and read users report, pass Canvas user ID to file quota function; write results to file

def read_users(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        f = open('file_quota.csv', 'w')
        f.write('%s, %s, %s, %s, %s, %s \n' % ('Canvas ID', 'SIS ID',
            'Email', 'First Name', 'Last Name', 'Total Files'))

        for row in  readCSV:

            if row[0] != 'canvas_user_id':
                canvas_id = row[0]
                sis_id = row[1]
                email = row[4]
                first_name = row[5]
                last_name = row[6]
                total_files = user_file_quota(canvas_id)
                f.write('%s, %s, %s, %s, %s, %s \n' % (canvas_id, sis_id, email, first_name, last_name, total_files))
                time.sleep(.1) # Needed to avoid too many API requests per minute
        f.close

# function to call API to report user file storage, write value to CSV

def user_file_quota(canvas_id):
    print ('Canvas id is', canvas_id)
    request = requests.get(instance_url + '/users/'
        + str(canvas_id) + '/files/quota?as_user_id='
        + str(canvas_id), headers = header)
    print (request)
    if request.status_code == 200:
        response = request.json()
        quota_used = round(((response['quota_used']) / 1048576) ,2)
        print (str(quota_used) + 'MB')
        return (str(quota_used) + 'MB')
    else:
        return 'error' + request.status_code


start_report(account)
