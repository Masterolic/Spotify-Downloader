from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from mbot import Mbot
import requests 

import os


API = "https://apis.xditya.me/lyrics?song="

@Mbot.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
        if not message.reply_to_message:
          await message.reply_text("Please reply to a message **Note** use %20 as space between words")
        else:          
          mee = await message.reply_text("`Searching 🔎 **Note** %20 as space between words `")
          song = message.reply_to_message.text
          chat_id = message.from_user.id
          rpl = lyrics(song)
          await mee.delete()
          try:
            await mee.delete()
            await bot.send_message(chat_id, text = rpl, reply_to_message_id = message.message_id, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs ", url = f"t.me/Spotify_downloa")]]))
          except Exception as e:                            
             await message.reply_text(f"I Can't Find A Song With `{song}` **note **use %20 as space between words", quote = True, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url = f"t.me/spotify_downloa")]]))



def search(song):
        r = requests.get(API + song)
        find = r.json()
        return find
       
def lyrics(song):
        fin = search(song)
        text = f'**🎶 Successfully Extracted Lyrics Of {song} 🎶**\n\n'
        text += f'`{fin["lyrics"]}`'
        text += '\n\n\n**Made By @spotify_downloa_bot**'
        return text
