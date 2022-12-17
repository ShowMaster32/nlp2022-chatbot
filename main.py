import threading
from datetime import date
from telegramGet import telegram_bot_getUpdates

# Running a check every 30seconds to see whether the Twitch stream is online
def main():
	timertime=5
	telegram_bot_getUpdates()
   
	# 5sec timer
	threading.Timer(timertime, main).start()
	
# Run the main function
if __name__ == "__main__":
	main()