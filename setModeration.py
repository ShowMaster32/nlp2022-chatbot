import os
import requests
import json
from telegramSend import telegram_bot_sendtext
from dotenv import load_dotenv

load_dotenv()

# Twitch client API parameters
twitchclient_id = os.getenv('TWITCHCLIENT_ID')
twitchsecret = os.getenv('TWITCHSECRET')

#exclude general keywords
banned_keyword_list = ['would', 'watch', 'want', 'start', 'stop', 'show']

#2. Add moderator
def addModerator(userStream):

	#filter text without banned_keyword_list words
	if userStream.casefold() in banned_keyword_list or len(userStream) < 4:
		return 'error'

	try:
		# URL to request OAuth Token
		tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + twitchclient_id + \
				   '&client_secret=' + twitchsecret+'&grant_type=client_credentials'


		response = requests.post(tokenurl)
		response.raise_for_status()
		OAuth_Token = response.json()["access_token"]

		getUserId = requests.get('https://api.twitch.tv/helix/users/?login=' + userStream, headers={'Authorization': 'Bearer ' + \
				   OAuth_Token,'Client-Id': twitchclient_id})
		print (json.loads(getUserId.content))
		
		var=json.loads(getUserId.content)
		print("Broadcaster id: ")
		print(var['data'][0]['id'])
		newModId=var['data'][0]['id']
		# Connection to Twitch
		response = requests.post('https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&user_id=' + newModId\
		
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		print (response.text)
				
		if 'user is already a mod' in response.text:
			telegram_bot_sendtext('User is already a mod!')
		elif len(response.text) == 0:
			telegram_bot_sendtext('Successfully added the moderator.')
		else:
			telegram_bot_sendtext('Something gone wrong')
		
		return 'done'
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"
	

#3. Function that reads moderators
def getModerators():
	try:
		# Connection to Twitch
		response = requests.get('https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') \
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		var=json.loads(response.content)
		print(var)
		
		message='Moderators list: \n'
		for index, user in enumerate(var['data']):
			place = index + 1
			message = message + str(place) + ') ' + user['user_name'] + '\n'
		
		telegram_bot_sendtext(message)
	
		return "Done"
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"
	

#4. Remove moderator
def removeModerator(userStream):

	#filter text without banned_keyword_list words
	if userStream.casefold() in banned_keyword_list or len(userStream) < 4:
		return 'error'

	try:
		# URL to request OAuth Token
		tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + twitchclient_id + \
				   '&client_secret=' + twitchsecret+'&grant_type=client_credentials'


		response = requests.post(tokenurl)
		response.raise_for_status()
		OAuth_Token = response.json()["access_token"]

		getUserId = requests.get('https://api.twitch.tv/helix/users/?login=' + userStream, headers={'Authorization': 'Bearer ' + \
				   OAuth_Token,'Client-Id': twitchclient_id})
		print (json.loads(getUserId.content))
		
		var=json.loads(getUserId.content)
		print("Broadcaster id: ")
		print(var['data'][0]['id'])
		newModId=var['data'][0]['id']
		# Connection to Twitch
		response = requests.delete('https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&user_id=' + newModId\
		
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		print (response.text)
		
		if 'user is not a mod' in response.text:
			telegram_bot_sendtext('User is not a mod!')
		elif len(response.text) == 0:
			telegram_bot_sendtext('Successfully removed the moderator.')
		else:
			telegram_bot_sendtext('Something gone wrong')
		
		return 'done'
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"