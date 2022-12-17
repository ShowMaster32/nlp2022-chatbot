import os
import requests
import json
from getStreamStatus import is_TwitchOnline

def telegram_bot_getUpdates():
	try:
		# Twitch API parameters
		bot_token = '5702349627:AAHpBV8Ez32bJqDTAKSoyJbiK1dajc6ISQ8'
		bot_chatID = '1671491209'
		
		
		getUp = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=-1'
		
		response = requests.get(getUp)
		r = json.loads(response.text)
		command = (r['result'][0]['message']['text']).casefold()
		dateCommand = (r['result'][0]['message']['date'])
		print (command)
		
		splittedCommand = command.split()
		
		if('online' in splittedCommand):
			print ('online')
		elif ('boh' in splittedCommand):
			is_TwitchOnline()
		else:
			print ('[' + str(dateCommand) + '] ' + command + ' -> Not a valid command')
	
	except Exception as e: 
		print(e)
	
	