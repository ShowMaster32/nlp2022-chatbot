import os
import requests
import json

# Function that sends a notification to telegram when stream is on/off-line
def telegram_bot_sendtext(bot_message):
	bot_token = '5702349627:AAHpBV8Ez32bJqDTAKSoyJbiK1dajc6ISQ8'
	bot_chatID = '1671491209'
	
	
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
			  bot_chatID + '&parse_mode=Markdown&text=' + bot_message

	response = requests.get(send_text)

	return response.json()