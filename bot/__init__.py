from os import environ,path
from dotenv import load_dotenv

if path.exists("config.env"):
    load_dotenv("config.env")


API_ID = str(environ.get("API_ID"))
API_HASH = str(environ.get("API_HASH"))
BOT_TOKEN = str(environ.get("BOT_TOKEN"))
SPOTIPY_CLIENT_ID = str(environ.get("SPOTIPY_CLIENT_ID","4fe3fecfe5334023a1472516cc99d805"))
SPOTIPY_CLIENT_SECRET = str(environ.get("SPOTIPY_CLIENT_SECRET","0f02b7c483c04257984695007a4a8d5c"))
DEEZER_PASSWORD = str(environ.get("DEEZER_PASSWORD"))
DEEZER_EMAIL = str(environ.get("DEEZER_EMAIL"))
DATABASE_URL = str(environ.get("DATABASE_URL"))
UPDATES_CHANNEL = str(environ.get("UPDATES_CHANNEL",None))
LOG_GROUP = str(environ.get("LOG_GROUP",None))
AUTH_CHATS = str(environ.get("AUTH_CHATS","-1001543575981")).split(" ")
for i in range(len(AUTH_CHATS)):
    AUTH_CHATS[i] = int(AUTH_CHATS[i])
