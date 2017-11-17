# Python 3 script to set users as account admins

import requests # requests module must be installed in python environment
import json # needed to format results for display or export
import csv # needed to read/write csv files
from pprint import pprint

log_filename = 'add_admins_log.txt'	# File to store status results
csv_filename = 'add_admins_list.csv' # File of source data
# add_admins_lisr CSV includes account ID, user ID, and role name

user = {
	'account_url':'https://seattleu.instructure.com',
	'token':'<INSERT TOKEN HERE>' 		# Example: 1~13eoncw39f32080234hnv230850KLJ823n8H
}
api_path = ['/api/v1/accounts/', '/admins']

header = {"Authorization" : "Bearer " + user['token']}

if __name__ ==  '__main__':
	with open(csv_filename, 'U') as csv_file:
		reader = csv.reader(csv_file)
		for rows in reader:
			account = 'sis_account_id:' + rows[0]
			adminId = 'sis_user_id:' + rows[1]
			role = rows[2]
			print adminId + ", " + account
			print api_path[0] + account + api_path[1]
			payload = {'user_id' : adminId, 'send_confirmation' : 0, 'role' : role}
			r = requests.post(user['account_url'] + api_path[0] + account + api_path[1], headers=header, params=payload)
			rjson = json.loads(r.text)
			print rjson
			print "Added " + rjson['user']['name']
			log = open(log_filename, 'a')
			log.write('Added ' + rjson['user']['name'] + ' (' + adminId + ')\n' )
			log.close()
