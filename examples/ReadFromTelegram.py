from telethon import TelegramClient, events, sync

# Remember to use your own values from my.telegram.org!
api_id = ...
api_hash = '...'
client = TelegramClient('anon', api_id, api_hash)

@client.on(events.NewMessage(chats='channel_name'))
async def my_event_handler(event):
    print(event.raw_text)

client.start()
client.run_until_disconnected()