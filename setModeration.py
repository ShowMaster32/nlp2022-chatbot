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
banned_keyword_list = ['clip', 'create', 'watch', 'want', 'start', 'please', 'online', 'know', 'stream', 'stop','show', 'from', 'by', 'where', 'when', 'because', 'while', 'what', 'make', 'would', 'will', 'might', 'may', 'can', 'could', 'shall', 'should', 'must', 'like', 'have', 'had', 'does']
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

		if var['data']:
			message='Moderators list: \n'
			for index, user in enumerate(var['data']):
				place = index + 1
				message = message + str(place) + ') ' + user['user_name'] + '\n'
		else:
			message='There are no moderators at the moment'

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


#5. Function that reads banned users
def getBannedUsers():
	try:
		# Connection to Twitch
		response = requests.get('https://api.twitch.tv/helix/moderation/banned?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') \
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		var=json.loads(response.content)
		print(var)

		if var['data']:
			message='Banned users\' list: \n'
			for index, user in enumerate(var['data']):
				place = index + 1
				message = message + str(place) + ') ' + user['user_name'] + '\n'
		else:
			message='There are no banned users at the moment'

		telegram_bot_sendtext(message)
	
		return "Done"
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"


#6. Function that ban a user
def banUser(userStream):

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
		userId=var['data'][0]['id']
		
		body = {"data": {"user_id":userId}}

		# Get banned users
		response = requests.get('https://api.twitch.tv/helix/moderation/banned?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') \
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		var=json.loads(response.content)

		already_banned = False
		for index, user in enumerate(var['data']):
			userName = user['user_name']
			if userName.casefold() == userStream.casefold():
				already_banned = True
				break
		
		if already_banned == False:
			# Connection to Twitch
			response = requests.post('https://api.twitch.tv/helix/moderation/bans?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&moderator_id=' + os.getenv('ADMIN_BROADCASTER_ID')\
					, headers={'Authorization': 'Bearer ' + \
					os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')}, json=body)

			var=json.loads(response.content)
			
			if var['data']:
				telegram_bot_sendtext('Successfully banned user.')
			else:
				telegram_bot_sendtext('Something gone wrong')
		else:
			telegram_bot_sendtext('The user is already banned!')

		return 'done'
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"


#7. Function that unban a user
def unbanUser(userStream):

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
		userId=var['data'][0]['id']
		
		response = requests.delete('https://api.twitch.tv/helix/moderation/bans?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&moderator_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&user_id=' + userId\
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		#print (response.text)
		
		if 'is not banned' in response.text:
			telegram_bot_sendtext('User is not banned!')
		elif len(response.text) == 0:
			telegram_bot_sendtext('Successfully unbanned user.')
		else:
			telegram_bot_sendtext('Something gone wrong')
		
		return 'done'
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"


#8. Function that reads VIP users
def getVips():
	try:
		# Connection to Twitch
		response = requests.get('https://api.twitch.tv/helix/channels/vips?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') \
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		var=json.loads(response.content)
		print(var)
		if var['data']:
		
			message='VIP users\' list: \n'
			for index, user in enumerate(var['data']):
				place = index + 1
				message = message + str(place) + ') ' + user['user_name'] + '\n'
		else:
			message="There are no VIPs at the moment"
		
		telegram_bot_sendtext(message)
	
		return "Done"
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"

#9. Add VIP user
def addVip(userStream):

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
		response = requests.post('https://api.twitch.tv/helix/channels/vips?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&user_id=' + newModId\
		
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		print (response.text)
				
		if 'The ID in ' in response.text and 'was not found' in response.text:
			telegram_bot_sendtext('The ID was not found!')
		elif len(response.text) == 0:
			telegram_bot_sendtext('Successfully added the VIP.')
		elif 'status' in response.text and '409' in response.text:
			telegram_bot_sendtext('The broadcaster does not have available VIP slots')
		elif 'status' in response.text and '422' in response.text:
			telegram_bot_sendtext('The user is a moderator. To make them a VIP, you must first remove them as a moderator')
		else:
			telegram_bot_sendtext('Something gone wrong')
		
		return 'done'
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"


#10. Remove VIP user
def removeVip(userStream):

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
		response = requests.delete('https://api.twitch.tv/helix/channels/vips?broadcaster_id=' + os.getenv('ADMIN_BROADCASTER_ID') + '&user_id=' + newModId\
				   , headers={'Authorization': 'Bearer ' + \
				   os.getenv('ACCESS_TOKEN'),'Client-Id': os.getenv('CLIENT_ID')})

		print (response.text)
		
		if 'The ID in ' + newModId + ' was not found.' in response.text:
			telegram_bot_sendtext('The ID was not found!')
		elif len(response.text) == 0:
			telegram_bot_sendtext('Successfully removed the VIP status from the user.')
		else:
			telegram_bot_sendtext('Something gone wrong')
		
		return 'done'
		
	except Exception as e: 
		print(e)
		return 'error'
	
	return "Done"