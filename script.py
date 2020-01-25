
#-*- coding: utf-8 -*-
'''
Tech Spec of Batch Inviter	

Input a list of emails (on a text document for example) - Check

Read those emails onto an array - Check

Invite people (rate limited) - check

When the invalid error message is returned stop - check

Ping every 5 seconds

If it allows, then keep sending rate limited emails - check

Have a dashboard of sorts that shows which ones are sent and which ones are haven’t'''

import requests
import json
import time
import ratelimit
from ratelimit import limits, sleep_and_retry
import csv


#Constants
token = "xoxp-908939173762-923938115046-921726053936-53f9396973a04bf9e2c3d0577b35a9cc"
channel = "CT3MZKFB7"
fileName = "emails.csv"
writeName = "emailsDone.csv"

def inputEmails():
	with open(fileName) as file_in:
		for email in file_in:
			emailList.append(email)

ONE_MINUTE = 60
@limits(calls = 240, period = ONE_MINUTE)
def APICall(email, real_name):
	response = requests.get('https://slack.com/api/users.admin.invite?token=' + token + '&email=' + email + "&channels=" + channel + "&real_name=" + real_name)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None


def batchInvite():
	with open(fileName) as csvFile:
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		for row in reader:
			email = str(row[0])
			real_name = str(row[1])
			if row[2] != 1:
				print(email)
				print(real_name)
				work = 0

				while (work == 0):
					try:
						result = APICall(email, real_name)
						print(result)
						if result["ok"] == False:
							if result["error"] == "invite_limit_reached":
								time.sleep(0.2)
							elif result["error"] == "already_in_team" or result["error"] == "already_invited" or result["error"] == "already_in_team_invited_user":
								work = 1

						elif result["ok"] == True:
							work = 1
							with open(writeName, 'a') as f:
							    writer = csv.writer(f)
							    writer.writerow([email, "1"])
					except ratelimit.RateLimitException:
						pass
			    		
  

def main():
	batchInvite()


main()

'''
Error codes to keep track of
Do Nothing
	- already_in_team
	- already_invited
	- 

Query for:
	- Channel: channel_not_found

Store:
	- invalid_email	

???
	- not_allowed




#to-do 
#use a URL formatter to make the above look prettier
# add flags in the python for different things
#requesto through terminal inputs for token and channel
'''


