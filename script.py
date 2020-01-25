import requests
import json
import time
import ratelimit
from ratelimit import limits, sleep_and_retry
import csv
import sys


#Constants

'''
Create a Slakc Legacy Token and use that as your token
Channel = the channel if od the channel you want your user to be invited into
fileName = input file of the emails
writeName = putput files of emails that have received invites
'''
token = ""
channel = "CT3MZKFB7"
fileName = "emails.csv"
writeName = "emailsDone.csv"

readEmails = set()

#Rate limited calls to the API 
TWO_SECONDS = 2
@limits(calls = 1, period = TWO_SECONDS)
def APICall(email, real_name):
	response = requests.get('https://slack.com/api/users.admin.invite?token=' + token + '&email=' + email + "&channels=" + channel + "&real_name=" + real_name)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None

def tryEmail(email, real_name):
	while True:
		try:
			result = APICall(email, real_name)
			print(result)
			if result["ok"] == False:
				if result["error"] == "invite_limit_reached":
					time.sleep(0.2)
				elif result["error"] == "already_in_team" or result["error"] == "already_invited" or result["error"] == "already_in_team_invited_user":
					return
				else:
					errorMessage = email + " failed because of: " + str(result["error"])
					sys.exit(errorMessage)


			elif result["ok"] == True:
				with open(writeName, 'a') as f:
				    writer = csv.writer(f)
				    writer.writerow([email, "1"])
				return
		except ratelimit.RateLimitException:
			pass



def batchInvite():
	with open(fileName) as csvFile:
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		for row in reader:
			email = str(row[0])
			real_name = str(row[1])
			if email not in readEmails:
				if row[2] != 1:
					print(email)
					print(real_name)
					tryEmail(email, real_name)


		
			    	
def main():
	with open(writeName) as csvFile:
		ogReader = csv.reader(csvFile, delimiter=',', quotechar='"')
		for row in ogReader:
			readEmails.add(row[0])
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
