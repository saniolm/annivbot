import time
import tweepy

def get_url(md,yr,cfg):
	return 'https://api.themoviedb.org/3/discover/tv?vote_count_gte='+str(cfg['MIN_VOTE_COUNT'])+'&first_air_date.gte='+str(yr)+'-'+md+'&first_air_date.lte='+str(yr)+'-'+md+'&api_key='+cfg['DB_APIKEY']

def process_data(data,age,api,cfg):
	for i in data['results']:
		list_movie=True
		
		if i['vote_count'] < cfg['MIN_VOTE_COUNT']:
			list_movie=False
		for gid in i['genre_ids']:
			if gid == 99:
				list_movie=False
			
		if list_movie == True:
			# len: xxxth: (6) title (yy) newline (1) url (24) = (140) > yy=114
			twt_txt=str(age)+'th: '+i['name'][:114]+'\nhttps://www.themoviedb.org/tv/'+str(i['id'])
				
			try:
				if cfg['TW_ENABLED']==True and cfg['DRY_RUN']==False:
					api.update_status(twt_txt)
				print(twt_txt)
				print(' - vote count: '+str(i['vote_count']))
			except tweepy.TweepError:
				print("Update Error")
			time.sleep(30)
			