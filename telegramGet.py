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

#import nltk necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only

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
			
			if re.search("hi", command) or re.search("hello", command) or re.search("hey", command) or re.search("good morning", command) or re.search("good afternoon", command) or re.search("good evening", command):  
				telegram_bot_sendtext("Hi, I'm a chat bot that let you interact with Twitch. Tell me something or type _help_ to see the list of available commands.")
			#search keyboards in chat to get info stream status:
			elif re.search("watch", command) or re.search("stream", command) or re.search("online", command):  
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
			elif re.search("help", command) or re.search("commands", command):
				telegram_bot_sendtext("Here the list of available commands: \n• watch _streamer username_ -> to get a link to watch a streamer \n• clip _streamer username_ -> to generate a clip of a streamer \n• top N categories -> to get the top N categories streamed \n• admin -> to enter admin mode")
			elif re.search("mod", command) or re.search("ban", command) or re.search("vip", command):
				telegram_bot_sendtext("Command available only into the admin mode. Type _admin_ to enter admin mode.")
			elif re.search("admin", command) or re.search("administrator", command) or re.search("administration", command):
				#welcome on admin menu function - admin menu
				telegram_bot_sendtext("Welcome to admin's menu. To quit menu, digit _quit_ word. To get the available command type _help_")
				print ("ADMIN Menu - Mode")
				lastMessageId = ""
				while True:
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

							result=''
							for split in splittedCommand:

								if len(split) >= 2 and split != "add" and split != "mod" and split != "moderator" and split != "moderators" and split != "admin":
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

							result=''
							for split in splittedCommand:
								
								if len(split) >= 2 and split != "remove" and split != "delete" and split != "mod" and split != "moderator" and split != "moderators" and split != "admin":
									print ("Trying to remove user: " + split)
									result = removeModerator(split)
									if result == 'done':
										break
							if result == 'error':
								message= 'The user you insert could not exist, try again with another. \n'
								telegram_bot_sendtext(message)
								
						#get list of moderators function - admin menu									
						elif re.search("list", command) and (re.search("mod", command) or re.search("moderator", command) or re.search("moderators", command) or re.search("people", command) or re.search("guys", command) or re.search("guy", command)):
							print ("Received listing moderators request")
							result = getModerators()
							
							if result == 'error':
								message= 'It seems there is an error while getting mod\'s list. \n'
								telegram_bot_sendtext(message)
								
						#get list of banned users - admin menu									
						elif re.search("list", command) and (re.search("banned", command) or re.search("ban", command)) and (re.search("users", command) or re.search("user", command) or re.search("people", command) or re.search("guys", command) or re.search("guy", command)):
							print ("Received listing banned users request")
							result = getBannedUsers()
							
							if result == 'error':
								message= 'It seems there is an error while getting banned users\'s list. \n'
								telegram_bot_sendtext(message)
																				
						#UNban user function - admin menu					
						elif (re.search("unban", command) and (re.search("user", command) or re.search("users", command))) or (re.search("remove", command) and re.search("ban", command) and (re.search("user", command) or re.search("users", command))):
							print ("Received unban user request")

							result=''
							for split in splittedCommand:
								
								if len(split) >= 2 and split != "remove" and split != "delete" and split != "mod" and split != "moderator" and split != "moderators" and split != "admin" and split !="user" and split != "users" and split != "unban" and split != "ban":
									
									print ("Trying to unban a user: " + split)
									result = unbanUser(split)
									if result == 'done':
										break
							if result == 'error':
								message= 'The user you insert could not exist, try again with another. \n'
								telegram_bot_sendtext(message)

						#ban user function - admin menu					
						elif re.search("ban", command) and (re.search("user", command) or re.search("users", command)):
							print ("Received ban user request")

							result=''
							for split in splittedCommand:
								
								if len(split) >= 2 and split != "remove" and split != "delete" and split != "mod" and split != "moderator" and split != "moderators" and split != "admin" and split !="user" and split != "users" and split != "ban":
									
									print ("Trying to ban a user: " + split)
									result = banUser(split)
									if result == 'done':
										break
							if result == 'error':
								message= 'The user you insert could not exist, try again with another. \n'
								telegram_bot_sendtext(message)
								
						#get list of VIP users - admin menu									
						elif re.search("list", command) and (re.search("vip", command) or re.search("vips", command)) and (re.search("users", command) or re.search("user", command) or re.search("people", command) or re.search("guys", command) or re.search("guy", command)):
							print ("Received listing VIP users request")
							result = getVips()
							
							if result == 'error':
								message= 'It seems there is an error while getting VIPs users\'s list. \n'
								telegram_bot_sendtext(message)	
								
						#add vip user function - admin menu
						elif re.search("add", command) and (re.search("vip", command) or re.search("vips", command)):
							print ("Received adding VIP user request")
							
							result=''
							for split in splittedCommand:
								
								if len(split) >= 2 and split != "add" and split != "vip" and split != "vips" and split != "admin":
									#check streaming status function
									print ("Trying to add VIP user: " + split)
									result = addVip(split)
									if result == 'done':
										break
							if result == 'error':
								message= 'The user you insert could not exist, try again with another one. \n'
								telegram_bot_sendtext(message)
										
						#remove vip user function - admin menu					
						elif (re.search("remove", command) or re.search("delete", command)) and (re.search("vip", command) or re.search("vips", command)):
							print ("Received removing VIP user request")

							result=''
							for split in splittedCommand:
								if len(split) >= 2 and split != "remove" and split != "delete" and split != "vip" and split != "vips" and split != "admin":
									
									print ("Trying to remove VIP user: " + split)
									result = removeVip(split)
									if result == 'done':
										break
							if result == 'error':
								message= 'The user you insert could not exist, try again with another. \n'
								telegram_bot_sendtext(message)
								
						elif re.search("help", command) or re.search("commands", command):
							telegram_bot_sendtext("Here the list of available admin commands: \n• add mod _username_ -> to add a moderator to your channel \n• remove mod _username_ -> to remove a moderator to your channel \n• list mod users -> to see the moderators of your channel \n• add ban _username_ -> to ban a user \n• remove ban _username_ -> to unban a user \n• list banned users -> to see the list of banned users \n• add vip _username_ -> to add a vip to your channel \n• remove vip _username_ -> to remove a vip to your channel \n• list vip users -> to see the vip of your channel \n")		
						elif re.search("watch", command) or re.search("clip", command) or re.search("top", command) or re.search("categories", command) or re.search("best", command) or re.search("games", command):
							telegram_bot_sendtext("Command not available into the admin mode. Type _quit_ to exit.")
						elif re.search("quit", command):
							print ("Command quit received. Exiting from admin's menu..")
							telegram_bot_sendtext("Command quit received. Exiting from admin's menu..")
							break
						else:
							if not re.search("admin", command):
								print ('[' + str(dateCommand) + '] ' + command + ' -> Not a valid ADMIN-command\n')
								telegram_bot_sendtext('*'+command + '* is not a valid ADMIN-command\n''Type _help_ to see the available commands.')
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
				print ('[' + str(dateCommand) + '] ' + command + ' -> Not a valid command\n')
				enableBot(command);
                #telegram_bot_sendtext('*'+command + '* is not a valid command\n''Type _help_ to see the available commands.')
	except Exception as e: 
		print(e)
	

#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return telegram_bot_sendtext(robo_response)

telegram_bot_sendtext("My name is Meliodas. I will answer your queries about Chatbots. If you want to exit, type Bye!")
def enableBot(user_response):
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            telegram_bot_sendtext("You are welcome..")
        else:
            if(greeting(user_response)!=None):
                telegram_bot_sendtext(reeting(user_response))
            else:
                telegram_bot_sendtext(response(user_response))
                sent_tokens.remove(user_response)
    else:
        telegram_bot_sendtext("Bye! take care..")    
        
        
