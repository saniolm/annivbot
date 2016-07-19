import time
import tweepy

def get_url(md,yr,cfg):
	return 'https://api.themoviedb.org/3/discover/movie?vote_count_gte='+str(cfg['MIN_VOTE_COUNT'])+'&include_adult='+str(cfg['INCLUDE_ADULT'])+'&primary_release_date.gte='+str(yr)+'-'+md+'&primary_release_date.lte='+str(yr)+'-'+md+'&api_key='+cfg['DB_APIKEY']

def process_data(data,age,api,cfg):
	for i in data['results']:
		list_item=True
			
		if i['adult'] == True:
			list_item=cfg['INCLUDE_ADULT']
		if i['vote_count'] < cfg['MIN_VOTE_COUNT']:
			list_item=False
		for gid in i['genre_ids']:
			if gid == 99:
				list_item=False
			
		if list_item == True:
			# len: xxxth: (6) title (yy) newline (1) url (24) = (140) > yy=114
			twt_txt=str(age)+'th: '+i['title'][:114]+'\nhttps://www.themoviedb.org/movie/'+str(i['id'])
				
			try:
				if cfg['TW_ENABLED']==True and cfg['DRY_RUN']==False:
					api.update_status(twt_txt)
				print(twt_txt)
				print(' - vote count: '+str(i['vote_count']))
			except tweepy.TweepError:
				print("Update Error")
			time.sleep(30)
			