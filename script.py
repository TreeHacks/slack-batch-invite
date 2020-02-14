import requests
import json
import time
import ratelimit
from ratelimit import limits, sleep_and_retry
import csv
import sys


#Constants

'''
Create a Slack Legacy Token and use that as your token
Channel = the channel if od the channel you want your user to be invited into
fileName = input file of the emails
writeName = putput files of emails that have received invites
'''
token = "insert token here"
channel = "CRS93299C"
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
				#if already in team, still mark it as done, just don't send out an API call
				elif result["error"] == "already_in_team" or result["error"] == "already_invited" or result["error"] == "already_in_team_invited_user" or result["error"] == "internal_error":
					with open(writeName, 'a') as f:
					    writer = csv.writer(f)
					    writer.writerow([email, real_name, result["error"]])
					return
				else:
					#if another error, break and alert me
					errorMessage = email + " failed because of: " + str(result["error"])
					sys.exit(errorMessage)


			#If it's good, send out the api call, and mark it as done by writing to CSV
			elif result["ok"] == True:
				with open(writeName, 'a') as f:
				    writer = csv.writer(f)
				    writer.writerow([email, real_name])
				return
		except ratelimit.RateLimitException:
			pass



def batchInvite():
	with open(fileName) as csvFile:
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		next(reader) #skips the first row (header)
		for row in reader:
			email = str(row[2])
			real_name = str(row[3])
			if email not in readEmails:
				print(email) #For debugging
				print(real_name) #For debugging
				tryEmail(email, real_name)


		
			    	
def main():
	#This first read is done so we have a list of emails that have already been read
	with open(writeName) as csvFile:
		ogReader = csv.reader(csvFile, delimiter=',', quotechar='"')
		for row in ogReader:
			readEmails.add(row[0])
	batchInvite()

main()




#to-do 
#use a URL formatter to make the above look prettier
# add flags in the python for different things
#requesto through terminal inputs for token and channel



