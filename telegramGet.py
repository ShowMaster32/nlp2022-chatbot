import os
import requests
import json
from telegramSend import telegram_bot_sendtext
from getStreamStatus import is_TwitchOnline
from dotenv import load_dotenv
import re

load_dotenv()

# Twitch API parameters
bot_token = os.getenv('BOT_TOKEN')
bot_chatID = os.getenv('BOT_CHATID')

def get_last_message_id():
	
	getUp = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=-1'
	
	response = requests.get(getUp)
	r = json.loads(response.text)
	messageId = r['result'][0]['message']['message_id']

	return messageId

lastMessageId = get_last_message_id()

def telegram_bot_getUpdates():
	try:
		getUp = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=-1'
		
		response = requests.get(getUp)
		r = json.loads(response.text)
		messageId = r['result'][0]['message']['message_id']
		global lastMessageId
		if messageId != lastMessageId:
			
			lastMessageId = messageId

			command = (r['result'][0]['message']['text']).casefold()
			dateCommand = (r['result'][0]['message']['date'])
			print (command)
			
			splittedCommand = command.split()
			
			#if('online' in splittedCommand):
			if re.search("online", command) or re.search("offline", command):  
				for split in splittedCommand:
					if len(split)>=2:
						result = is_TwitchOnline(split)
						if result == 'done':
							break
				if result == 'error':
					message= 'The user you insert could not exist, try again with another. \n'
					telegram_bot_sendtext(message)		
			elif ('boh' in splittedCommand):
				print('boh')
			else:
				print ('[' + str(dateCommand) + '] ' + command + ' -> Not a valid command')
	
	except Exception as e: 
		print(e)
	
	