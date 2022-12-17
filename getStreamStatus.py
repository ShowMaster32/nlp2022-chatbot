import os
import requests
import json
from telegramSend import telegram_bot_sendtext

#2. Function that checks whether stream is online
def is_TwitchOnline():
	try:
		# Twitch API parameters
		twitchclient_id="0t41emt7s7m1m6wrg0e7mco4ymikjp"
		twitchsecret="fyqm53eh0ufs250r01fs37oxhvjaa6"

		# The Twitch user you are interested in for example
		# https://www.twitch.tv/maximum  --> userStream='maximum'
		userStream='sh0wblack32'


		# URL to request OAuth Token
		tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + twitchclient_id + \
				   '&client_secret=' + twitchsecret+'&grant_type=client_credentials'


		response = requests.post(tokenurl)
		response.raise_for_status()
		OAuth_Token = response.json()["access_token"]

		# Connection to Twitch
		response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + \
				   userStream, headers={'Authorization': 'Bearer ' + \
				   OAuth_Token,'Client-Id': twitchclient_id})
		var=json.loads(response.content)


		# Dummy variable stored in text file for status update
		cwd = os.getcwd()
		filename= cwd + '/StreamTwitch_01Bot.txt'
		if (os.path.exists(filename) == False):
			f = open(filename, "w")
			f.write("FALSE")
			f.close()
		else:
			print("running..")    

		f = open(filename)
		boolean_online = f.read()
		f.close()

		# Twitch var data returns wether the stream just went live
		if var['data'] and boolean_online.upper()=='FALSE':
			message='Stream of : ['+str(userStream)+'](https://www.twitch.tv/'+str(userStream)+') is online. \n'


			telegram_bot_sendtext(message)
			f = open(filename, "w")
			f.write("TRUE")
			f.close()

		# Twitch var data returns wether the stream just went off-line    
		if not var['data'] and boolean_online.upper()=='TRUE':
			telegram_bot_sendtext(userStream.upper()+' is offline')
			f = open(filename, "w")
			f.write("FALSE")
			f.close()
	
	except Exception as e: 
		print(e)
	
	return "Done"