import os
import requests
import json
from telegramSend import telegram_bot_sendtext
from getStreamStatus import is_TwitchOnline
from setModeration import *
from createClip import createClip
from topGames import topGames
from dotenv import load_dotenv
import re
import time

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
	#adminMode = 0;
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
					if len(split) >= 2:
						#check streaming status function
						result = is_TwitchOnline(split)
						if result == 'done':
							break
				if result == 'error':
					message= 'The user you insert could not exist, try again with another. \n'
					telegram_bot_sendtext(message)
			elif re.search("clip", command):
				for split in splittedCommand:
					if len(split)>=2:
						result = createClip(split)
						if result == 'done':
							break
				if result == 'error':
					message= 'The user you insert could not exist, try again with another. \n'
					telegram_bot_sendtext(message)
			#get top N categories at the moment
			elif re.search("top", command) or re.search("best", command) or re.search("games", command) or re.search("categories", command):
				done = False
				for split in splittedCommand:
					if re.search('[0-9]+', split):
						topGames(split)
						done = True
						break
				if not done:
					topGames(10)
			elif re.search("admin", command) or re.search("administrator", command) or re.search("administration", command):
				#welcome on admin menu function - admin menu
				telegram_bot_sendtext("Welcome to admin's menu. To quit menu, digit \":quit\" word.")
				print ("ADMIN Menu - Mode")
				lastMessageId = ""
				while True:
					#TODO: unire in una funzione unica ###########################################
					getUp = 'https://api.telegram.org/bot' + bot_token + '/getUpdates?offset=-1'
					response = requests.get(getUp)
					r = json.loads(response.text)
					messageId = r['result'][0]['message']['message_id']
					if messageId != lastMessageId:
						
						lastMessageId = messageId

						command = (r['result'][0]['message']['text']).casefold()
						dateCommand = (r['result'][0]['message']['date'])
						print (command)
			
						splittedCommand = command.split()
						##########################################################################
							
						#add moderators function - admin menu
						if re.search("add", command) and (re.search("mod", command) or re.search("moderator", command) or re.search("moderators", command)):
							print ("Received adding moderators request")

							for split in splittedCommand:
								if len(split) >= 2 and split != "add" and split != "mod" and split != "moderator" and split != "moderators" and split != "admin":
									#check streaming status function
									print ("Trying to add user: " + split)
									result = addModerator(split)
									if result == 'done':
										break
									if result == 'error':
										message= 'The user you insert could not exist, try again with another one. \n'
										telegram_bot_sendtext(message)
										
						#remove moderators function - admin menu					
						elif (re.search("remove", command) or re.search("delete", command)) and (re.search("mod", command) or re.search("moderator", command) or re.search("moderators", command)):
							print ("Received removing moderators request")

							for split in splittedCommand:
								if len(split) >= 2 and split != "remove" and split != "delete" and split != "mod" and split != "moderator" and split != "moderators" and split != "admin":
									#check streaming status function
									print ("Trying to remove user: " + split)
									result = removeModerator(split)
									if result == 'done':
										break
									if result == 'error':
										message= 'The user you insert could not exist, try again with another. \n'
										telegram_bot_sendtext(message)
								
						#get list of moderators function - admin menu									
						elif re.search("list", command) and (re.search("mod", command) or re.search("moderator", command) or re.search("moderators", command)):
							print ("Received listing moderators request")
							result = getModerators()
							
							if result == 'error':
								message= 'It seems there is an error while getting mod\'s list. \n'
								telegram_bot_sendtext(message)
								
						elif re.search("quit", command):
							print ("Command quit received. Exiting from admin's menu..")
							telegram_bot_sendtext("Command quit received. Exiting from admin's menu..")
							break
						else:
							print ('[' + str(dateCommand) + '] ' + command + ' -> Not a valid ADMIN-command')
							continue
						print ("Sleeping until next command..")
						time.sleep(3)
					else:
						print ("...")
						time.sleep(5)
						continue
			elif re.search("quit", command):
				exit()
			else:
				print ('[' + str(dateCommand) + '] ' + command + ' -> Not a valid command')
	
	except Exception as e: 
		print(e)
	
	