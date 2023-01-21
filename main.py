import threading
from datetime import date
from telegramGet import telegram_bot_getUpdates

def main():
	timertime=1
	telegram_bot_getUpdates()
   
	# 5sec timer
	threading.Timer(timertime, main).start()
	
# Run the main function
if __name__ == "__main__":
	main()