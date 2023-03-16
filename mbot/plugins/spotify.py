from pyrogram.errors import FloodWait,Forbidden,UserIsBlocked,MessageNotModified,ChatWriteForbidden
from requests.exceptions import MissingSchema
from asyncio import sleep
#from mbot.utils.progress import progress
import time
from mutagen.id3 import ID3, APIC,error
from mutagen.easyid3 import EasyID3
from mbot import AUTH_CHATS, LOGGER, Mbot,LOG_GROUP,BUG
from pyrogram import filters,enums
from mbot.utils.mainhelper import parse_spotify_url,fetch_spotify_track,download_songs,thumb_down,copy,forward 
from mbot.utils.ytdl import getIds,ytdl_down,audio_opt
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
#import psutil
from os import mkdir
from os import environ
import shutil
from shutil import rmtree
#from Script import script
from random import randint
#import random
#import eyed3 
from mutagen.easyid3 import EasyID3
#import eyed3
from lyricsgenius import Genius 
from pyrogram.types import Message
from pyrogram.errors.rpc_error import RPCError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
#import psutil
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
#from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS
#from database.users_chats_db import db
#from database.ia_filterdb import Media
#from utils import temp
#from Script import script
from pyrogram.errors import ChatAdminRequired
from mbot import BUG,Mbot
from mutagen.mp3 import MP3
from requests.exceptions import MissingSchema
client = Spotify(auth_manager=SpotifyClientCredentials())
PICS = ("mbot/1162775.jpg mbot/danny-howe-bn-D2bCvpik-unsplash.jpg mbot/saurabh-gill-38RthwbB3nE-unsplash.jpg").split()
LOG_TEXT_P = """
ID - <code>{}</code>
Name - {}
"""
#PICS = ("mbot/1162775.jpg mbot/danny-howe-bn-D2bCvpik-unsplash.jpg mbot/saurabh-gill-38RthwbB3nE-unsplash.jpg").split()
@Mbot.on_message(filters.regex(r'https?://open.spotify.com[^\s]+') & filters.incoming | filters.regex(r'https?://open.spotify.com[^\s]+') & filters.command(["spotify","spotdl"]) | filters.incoming & filters.regex(r"spotify:") & filters.chat(AUTH_CHATS))
async def spotify_dl(_,message):
    link = message.matches[0].group(0)
    #seep = await sleep (0.9)
    m = await message.reply_text(f"⏳")
    n = await message.reply_chat_action(enums.ChatAction.TYPING)

    try:
        parsed_item = await parse_spotify_url(link)
        item_type, item_id = parsed_item[0],parsed_item[1]
        randomdir = f"/tmp/{str(randint(1,100000000))}"
        mkdir(randomdir)
        if item_type in ["show", "episode"]:
            items = await getIds(link)
            for item in items:
                # you can update this chat action #cForChat = await message.reply_chat_action("record_audio")
                sleeeps = await sleep (0.9)
                PForCopy = await message.reply_photo(item[5],caption=f"✔️ Episode Name : `{item[3]}`\n🕔 Duration : {item[4]//60}:{item[4]%60}")
                fileLink = await ytdl_down(audio_opt(randomdir,item[2]),f"https://open.spotify.com/episode/{item[0]}")
                thumbnail = await thumb_down(item[5],item[0])
                sleeping  = await sleep(2.0)
                DForChat =  await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                #reply = await message.reply_text(f"sorry we removed support of  episode 😔 pls send other types")
                AForCopy = await message.reply_audio(fileLink,title=item[3].replace("_"," "),performer="Spotify",duration=int(item[4]),caption=f"[{item[3]}](https://open.spotify.com/episode/{item[0]})",thumb=thumbnail,quote=True)
                shutil.rmtree(randomdir)
                if LOG_GROUP:
                    await sleep(3.5)
                    await copy(PForCopy,AForCopy)
            return await m.delete()
        elif item_type == "track":
            song = await fetch_spotify_track(client,item_id)
            # you can update to latest chat action #cForChat = await message.reply_chat_action("record_audio")
            #sleeeps = await sleep (0.9)
            PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}­`\n🎤 Artist : `{song['artist']}­`\n💽 Album : `{song['album']}­`\n🗓 Release Year: `{song['year']}­`")
            path = await download_songs(song,randomdir)
            thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
            dForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
            audio = EasyID3(path)
            try:
                audio["TITLE"] = f" {song.get('name')}"
                audio["originaldate"] = song.get('year')
              #  audio["YEAR_OF_RELEASE"] = song.get('year')
                audio["WEBSITE"] = "https://t.me/Spotify_downloa_bot"
            #    audio["GEEK_SCORE"] = "9"
                audio["ARTIST"] = song.get('artist')                                                                            
                audio["ALBUM"] = song.get('album')
                audio["DATE"] = song.get('year')
                audio.save()
                try:
                   audio = MP3(path, ID3=ID3)
                   audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnail,'rb').read()))
                   audio.save()
                except Exception :
                    pass   
            except:
                pass
            audio.save()
            AForCopy = await message.reply_audio(path,performer=f"{song.get('artist')}­",title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail, parse_mode=enums.ParseMode.MARKDOWN,quote=True)
            if LOG_GROUP:
                await sleep(2.5)
                await copy(PForCopy,AForCopy)
            return await m.delete()
        elif item_type == "playlist":
            tracks = client.playlist_items(playlist_id=item_id,additional_types=['track'], limit=40, offset=0, market=None)
            total_tracks = tracks.get('total')
            for track in tracks['items']:
                song = await fetch_spotify_track(client,track.get('track').get('id'))
                #you can update to latest chat action #cForChat = await message.reply_chat_action("record_audio")
               #sleeeps = await sleep (0.9)
                PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}­`\n🎤 Artist : `{song['artist']}­`\n💽 Album : `{song['album']}­`\n🗓 Release Year: `{song['year']}­`\n🔢 Track No: `{song['playlist_num']}­`\n🔢 Total Track: `{total_tracks}­`")
                path = await download_songs(song,randomdir)
                thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                cForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
                sleeping  = await sleep(0.8)
                audio = EasyID3(path)
                try:
                    audio["TITLE"] = f" {song.get('name')} "
                    audio["originaldate"] = song.get('year')
                #    audio["YEAR_OF_RELEASE"] = song.get('year')
                    audio["WEBSITE"] = "https://t.me/Spotify_downloa_bot"
              #      audio["GEEK_SCORE"] = "9"
                    audio["ARTIST"] = song.get('artist')                                                                           
                    audio["ALBUM"] = song.get('album')
                    audio["DATE"] = song.get('year')
                except:
                     pass
                audio.save()
                try:
                   audio = MP3(path, ID3=ID3)
                   audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnail,'rb').read()))
                except Exception as e:
                    pass
                audio.save()
                AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,quote=True)
                feedback = await message.reply_text(f"Done✅",   
                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Feedback", callback_data="feed")]]))
                if LOG_GROUP:
                    await sleep(2.5)
                    await copy(PForCopy,AForCopy)
            return await m.delete()
        elif item_type == "album":
            tracks = client.album_tracks(album_id=item_id, limit=40, offset=0, market=None)
            for track in tracks['items']:
                song = await fetch_spotify_track(client,track.get('id'))
               #sleeeps = await sleep (0.9)
                PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}­`\n🎤 Artist : `{song['artist']}­`\n💽 Album : `{song['album']}­`\nq🗓 Release Year: `{song['year']}­`")
                path = await download_songs(song,randomdir)
                thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                sleeping  = await sleep(0.8)
                audio = EasyID3(path)
                try:
                    audio["TITLE"] = f" {song.get('name')} "
                    audio["originaldate"] = song.get('year')
            #        audio["YEAR_OF_RELEASE"] = song.get('year')
                    audio["WEBSITE"] = "https://t.me/Spotify_downloa_bot"
              #      audio["GEEK_SCORE"] = "9"
                    audio["ARTIST"] = song.get('artist')                                                                         
                    audio["ALBUM"] = song.get('album')
                    audio["DATE"] = song.get('year')
                except:
                    pass
                audio.save()
                try:
                   audio = MP3(path, ID3=ID3)
                   audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnail,'rb').read()))
                except Exception as e:
                   pass
                   print(e)
                audio.save()
                AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,quote=True)
                feedback = await message.reply_text(f"Done✅",   
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Feedback", callback_data="feed")]]))
                if LOG_GROUP:
                    await sleep(2.5)
                    await copy(PForCopy,AForCopy)
            return await m.delete()
                   
    except Exception as e:
        LOGGER.error(e)
        K = await m.edit_text(e)
        H = await message.reply_text(f"Done✅",   
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Error Detected", callback_data="bug")]]))
        await message.reply_text(f"you can also get it from Saavn type /saavn music_name")
        if BUG:
           await forward(K,H)
    finally:
        await sleep(2.0)
        try:
            rmtree(randomdir)
        except:
            pass
        await message.reply_text(f"Done✅",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Feedback", callback_data="feed")]]))
        await message.reply_text(f"Check out @spotify_downloa (music)  @spotifynewss(News)")
@Mbot.on_callback_query(filters.regex(r"feed"))
async def feedback(_,query):
      await query.message.edit(f"Feedback 🏴‍☠️",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Press here", url="https://t.me/dailychannelsbot?start=spotify_downloa_bot")]]))

@Mbot.on_callback_query(filters.regex(r"bug"))                                                                                                          
async def bug(_,query):                                                                                                                                  
      await query.message.edit(f"please report to the dev with above error occurred message")
      await sleep(2.3)
      await query.message.edit(f"Bug Report 🪲",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Report to dev ", url="https://t.me/masterolic")]]))
