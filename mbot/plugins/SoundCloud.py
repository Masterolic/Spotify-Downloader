from pyrogram import filters,enums
from mbot import AUTH_CHATS, LOG_GROUP,Mbot
from os import mkdir
#from utils import temp
from random import randint
#from database.users_chats_db import db
from yt_dlp import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from mbot.utils.mainhelper import fetch_spotify_track
client_credentials_manager = SpotifyClientCredentials()
client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
async def get_data(query):
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,

        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(query, download=False)
            return video 

async def down_data(item,query):
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"{item['title']} {item['uploader']}.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,

        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
            video = ydl.extract_info(query, download=True)
            return ydl.prepare_filename(video)

@Mbot.on_message(filters.regex(r'https?://.*soundcloud[^\s]+'))
async def link_handler(Mbot, message):
    try:
      # if message.from_user.id in temp.BANNED_USERS:
       #   return
       m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
       await message.reply_chat_action(enums.ChatAction.TYPING)
       link = message.matches[0].group(0)
     #  get_s = await db.get_set(message.from_user.id)
    #   if get_s['http'] == "False":
     #     return
       item=await get_data(link)
       path=await down_data(item,link)
       await message.reply_audio(path)
       await m.delete()
       os.remove(path)
    except Exception as e:
        pass
        await message.reply(e)
    #    await Mbot.send_message(BUG,f"SoundCloud  {e}")
        await m.delete()
        os.remove(path)
