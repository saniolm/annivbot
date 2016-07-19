import time
import tweepy

def get_url(md,yr,cfg):
	return 'http://www.giantbomb.com/api/games/?api_key='+cfg['DB_APIKEY']+'&format=json&filter=original_release_date:'+str(yr)+'-'+md+'%2000:00:00'

def process_data(data,age,api,cfg):
	for i in data['results']:
		list_item=True
		if i['number_of_user_reviews'] < cfg['MIN_VOTE_COUNT']:
			list_item=False
			
		if list_item==True:
			# len: xxxth: (6) title (yy) newline (1) url (24) = (140) > yy=114
			twt_txt=str(age)+'th: '+i['name'][:114]+'\n'+i['site_detail_url']
				
			try:
				if cfg['TW_ENABLED']==True && cfg['DRY_RUN']==False:
					api.update_status(twt_txt)
				print(twt_txt)
				print(' - review count: '+str(i['number_of_user_reviews']))
			except tweepy.TweepError:
				print("Update Error")
			time.sleep(30)
			