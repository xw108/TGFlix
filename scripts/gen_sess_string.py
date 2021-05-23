import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id      = int(os.environ.get('TG_APP_ID') or input("Enter your telegram app id: "))
api_hash    = os.environ.get('TG_APP_HASH') or input("Enter your telegram app hash: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())