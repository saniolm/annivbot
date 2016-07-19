#!/usr/bin/env python3
# invoke by cron.d

import json
import tweepy
import urllib.request as ureq
import urllib.parse as par
import datetime
import time
import sys

try:
	bot = str(sys.argv[1])
except:
	bot='movie'
	
if bot == 'game':
	import bot_game as b
elif bot == 'movie':
	import bot_movie as b
elif bot == 'tv':
	import bot_tv as b
else:
	print('No such bot: '+bot)
	sys.exit()
	
def write_file(file,content):
	f = open(file, "w")
	f.write(str(content))
	f.close

def read_file(file):
	f = open(file, "r")
	content=f.read()
	f.close
	
	return content


def get_data(url):
	html = ureq.urlopen(url).read()
	data = json.loads(html.decode('utf-8'))
	return data

cfg = json.loads(read_file("config.json"))[bot]
try:
	cfg['DRY_RUN'] = bool(sys.argv[2])
except:
	cfg['DRY_RUN']=False


def main():

	td = datetime.date.today()
	md=td.strftime('%m-%d')
	yr=td.year
	ymd=str(yr)+'-'+md
	age=0
	lastpost=''
	lastpost_file='lastpost_'+bot+'.txt'
	
	auth = tweepy.OAuthHandler(cfg['TW_CONSUMER_KEY'], cfg['TW_CONSUMER_SECRET'])
	auth.set_access_token(cfg['TW_ACCESS_TOKEN'], cfg['TW_ACCESS_SECRET'])
	api = tweepy.API(auth)
	
	if cfg['DRY_RUN']==False:
		try:
			lastpost=read_file(lastpost_file)
		except:
			pass
	
	if lastpost==ymd:
		print("Already posted")
		return
	
	while yr>cfg['YEAR_BOUND']:
		yr-=5
		age+=5
		print(' >>> '+str(yr)+' ('+str(age)+' yrs)')

		url=b.get_url(md,yr,cfg)
		data=get_data(url)
	
		b.process_data(data,age,api,cfg)
		
		if cfg['DRY_RUN']==False:
			write_file(lastpost_file,ymd)
		
if __name__ == "__main__":
	main()