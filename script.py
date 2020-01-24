
#-*- coding: utf-8 -*-
'''
Tech Spec of Batch Inviter	

Input a list of emails (on a text document for example) - Check

Read those emails onto an array - Check

Invite people (rate limited)

When the invalid error message is returned stop

Ping every 5 seconds

If it allows, then keep sending rate limited emails

Have a dashboard of sorts that shows which ones are sent and which ones are haven’t'''

import requests
import json
import time


#Constants
token = "XXX"
channel = "C0000000"
fileName = "emails.txt"

emailList = []

#response = requests.get('https://slack.com/api/users.admin.invite?token=XXX&email=test@email.com&channels=C000000')

def inputEmails():
	with open(fileName) as file_in:
		for email in file_in:
			emailList.append(email)

def APICall(email):
	response = requests.get('https://slack.com/api/users.admin.invite?token=' + token + '&email=' + email + "&channels=" + channel)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None


def batchInvite():
	i = 0
	while (i < len(emailList)):
		email = emailList[i]
		time.sleep(0.2)
		result = APICall(email)

		print(email, result)
		
		if result["ok"] == True:
			if result["error"] == "invite_limit_reached":
				time.sleep(0.2)

		else:
			print(i)
			i = i + 1

def main():
	inputEmails()
	print(emailList)
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
# error handling with different status codes
# add flags in the python for different things
#proper rate limiting
'''


