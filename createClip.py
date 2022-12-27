import os
import time
import requests
import json
from telegramSend import telegram_bot_sendtext
from dotenv import load_dotenv

load_dotenv()

# Twitch client API parameters
twitchclient_id = os.getenv('TWITCHCLIENT_ID')
twitchsecret = os.getenv('TWITCHSECRET')
OAuth_edit_clip = os.getenv('OAUTH_TOKEN')
client_id_edit_clip = os.getenv('CLIENT_ID')

banned_keyword_list = ['clip', 'create', 'want', 'show', 'from', 'by', 'where', 'when', 'because', 'while', 'what']

#2. Function that checks whether stream is online
def createClip(userStream):

	#filter text without banned_keyword_list words
	if userStream.casefold() in banned_keyword_list or len(userStream) < 4:
		return 'error'

	try:
		
		# https://www.twitch.tv/maximum  --> userStream='maximum'

		# URL to request OAuth Token
		tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + twitchclient_id + \
				   '&client_secret=' + twitchsecret+'&grant_type=client_credentials'


		response = requests.post(tokenurl)
		response.raise_for_status()
		OAuth_Token = response.json()["access_token"]

		headers = {
			'Authorization': 'Bearer ' + OAuth_Token,
			'Client-Id': twitchclient_id
		}

		# 1) GET USER ID
		response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + \
				   userStream, headers=headers)

		stream=json.loads(response.content)

		if stream['data']:
			user_id = stream['data'][0]['user_id']

			# token OAuth generated with scope clip:edit https://twitchtokengenerator.com/?code=ib0zf1aoehm67rse2gmjtt0m8gh5pl&scope=clips%3Aedit&state=frontend%7CNy9ZS0hYT01rNFdEMk0xK0ZOd0M5UT09
			headers = {
				'Authorization': 'Bearer '+ OAuth_edit_clip,
				'Client-Id': client_id_edit_clip
			}
			
			# 2) CREATE THE CLIP
			response = requests.post('https://api.twitch.tv/helix/clips?broadcaster_id=' + \
					user_id, headers=headers)
			create_clip=json.loads(response.content)
			
			telegram_bot_sendtext('Creating the clip..')	
			time.sleep(6)

			if create_clip['data']:
				clip_id = create_clip['data'][0]['id']
				
				headers = {
					'Authorization': 'Bearer ' + OAuth_Token,
					'Client-Id': twitchclient_id
				}

				# 3) GET CLIP URL
				response = requests.get('https://api.twitch.tv/helix/clips?id='+clip_id, headers=headers)
				get_clip=json.loads(response.content)
				
				url_clip = get_clip['data'][0]['url']
				#telegram_bot_sendtext(message)
				telegram_bot_sendtext('Click [here]('+url_clip+') to watch the clip!')	
		# Twitch var data returns wether the stream just went off-line    
		if not stream['data']:
			telegram_bot_sendtext(userStream.upper()+' is offline, cannot create clip!')		

		return 'done'	
		
	except Exception as e: 
		print(e)
		return 'error'
		#message= userStream.upper()+' could not exist, try again with another. \n'
		#telegram_bot_sendtext(message)
