#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import time
import re
import csv
import random
import argparse
import sys

parser = argparse.ArgumentParser(description="""Just A scrapper""")

parser.add_argument("-k","--keyword",help="client keyword")
parser.add_argument("-c","--csv",help="write output in csvfile")
args = parser.parse_args()

keyword = args.keyword
csv = args.csv

if csv:
	if not csv.endswith(".csv"):
		print("Your file must end with .csv extension")
		sys.exit(1)

def output(quotes):
	csv_file = ''

	csv_file += 'User_url,username,servername,message,timestamp\n'

	for item in quotes:
		csv_file += str(item) + "\n"

	report = csv_file

	with open(csv, 'a') as f:
		f.write(report)
	f.close()


def discordleaks(req):
	soup = BeautifulSoup(req.content, 'html5lib')
	scrap = soup.find('div', attrs = {'class':'results'})
	final_results = []

	for user in scrap.findAll('div', attrs = {'class':'discord-message'}):
		data = {}
		data['url'] = user.a['href']

		for username in user.findAll('div', attrs = {'class':'discord-message-user-name'}):
			data['user_name'] = username.a.text
		for server in user.findAll('div', attrs = {'class':'discord-message-meta-items'}):
			data['server'] = server.a.text
		for mess in user.findAll('div', attrs = {'class':'discord-message-content'}):
			data['message'] = mess.p.text
		for timestamp in user.findAll('div', attrs = {'class':'discord-message-meta-items'}):
			data['time'] = timestamp.span.text

		final_results.append(data)

	if csv:
		output(final_results)
	else:
		print(final_results)





def request():
	with open('agents.txt','r') as file:

		lines = open('agents.txt').read().splitlines()

		header_value = random.choice(lines)

		header = {}

		header['User-Agent'] = header_value
		file.close()

		URL = ("https://discordleaks.unicornriot.ninja/discord/search?q=%s+&s=" % keyword)
		req = requests.get(URL, headers=header)
		discordleaks(req)
		soup = BeautifulSoup(req.content, 'html5lib')

		pages = soup.find('p', attrs = {'class':'pagination'})

		final = (re.search(r"/\d+",str(pages)).group()).strip("/")

		print("Total pages found:%s" % final)

		time.sleep(2)

		if final == 1:
			pass
		else:
			for page in range(2,int(final) + 1):
				print("Scrapping page %d data" % page)
				URL = ("https://discordleaks.unicornriot.ninja/discord/search?q=%s+&s=&page=%s" % (keyword,page))
				req = requests.get(URL, headers=header)
				discordleaks(req)

request()
