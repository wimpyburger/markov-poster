import subprocess as sp
import random
import praw
import time, threading

subreddit = "usersims"
exePath = "markov.exe"
users = ["sanimus", "thisisgilbates"]
user_agent = "usersims 1.0 by /u/plebmaster69"
r = praw.Reddit(user_agent=user_agent)
submitProbability = 0.1 # probability for bot to submit new post

def submitNew():
	title = ""
	content = ""
	tryCount = 0
	
	while tryCount < 5:
		# select random user
		user = random.choice(users)
		r.login("changeme", "changeme", disable_warning=True)
		txtPath = "text/" + user + ".txt"
		
		# random word
		word = "%RANDOM%"

		# get title
		cmd = exePath + " " + txtPath + " " + word
		test = sp.call(cmd)
		# get whats returned
		f = open('output.txt', "r")
		title = f.read()
		f.close()
		tryCount+=1
		
		# get content
		cmd = exePath + " " + txtPath + " " + word
		test = sp.call(cmd)
		# get whats returned
		f = open('output.txt', "r")
		content = f.read()
		f.close()
		
		tryCount+=1
		
		if title == "" or content == "":
			continue
		else:
			r.submit(subreddit, title, text=content)
			break
		
def postReply():
	submissions = r.get_subreddit(subreddit).get_new(limit=10)
	submissions = list(submissions)
	# select random recent submission
	submission = random.choice(submissions)
	words = submission.title.split() # remove garbage at start
	
	tryCount = 0
	content = ""
	
	while tryCount < 10:
		# select random user
		user = random.choice(users)
		r.login("changeme", "changeme", disable_warning=True)
		txtPath = "text/" + user + ".txt"
		
		# random word from the title
		word = random.choice(words)
		
		# get content
		cmd = exePath + " " + txtPath + " " + word
		test = sp.call(cmd)
		# get whats returned
		f = open('output.txt', "r")
		content = f.read()
		f.close()
		
		tryCount+=1
		
		if content == "":
			continue
		else:
			submission.add_comment(content)
			break

def main():
	# do every 10 minutes
	threading.Timer(600, main).start()
	# decide if to create new post or to 
	x = random.random()
	if x < submitProbability:
		submitNew()
	else:
		postReply()

main()