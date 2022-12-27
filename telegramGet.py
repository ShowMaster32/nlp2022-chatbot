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
print("Starting chatbot with bot token: " + bot_token + " and bot chatID: " + bot_chatID)

#get last message_id from telegram chat
def get_last_message_id():
	messageId = False
	try:
		getUp = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=-1'
		
		response = requests.get(getUp)
		r = json.loads(response.text)
		
		#check if r is empty -> case: {"ok":true,"result":[]}
		if not len(r['result']) == 0:
			messageId = r['result'][0]['message']['message_id']
			print("Last message id: ", end='')
			print(messageId)
		else:
			print("No messages found!")
			
	except Exception as e: 
		print(e)
		
	return messageId


lastMessageId = get_last_message_id()

#get last updates from telegram chat, call is_TwitchOnline to get streamer's stream status
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
			
			#search keyboards in chat to get info stream status:
			if re.search("watch", command) or re.search("stream", command):  
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
	
	