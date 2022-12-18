import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Twitch API parameters
bot_token = os.getenv('BOT_TOKEN')
bot_chatID = os.getenv('BOT_CHATID')

# Function that sends a notification to telegram when stream is on/off-line
def telegram_bot_sendtext(bot_message):	
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
			  bot_chatID + '&parse_mode=Markdown&text=' + bot_message

	response = requests.get(send_text)

	return response.json()