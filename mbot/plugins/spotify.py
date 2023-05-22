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
ADMINS = 1794941609
from requests.exceptions import MissingSchema
client = Spotify(auth_manager=SpotifyClientCredentials())
PICS = ("mbot/1162775.jpg mbot/danny-howe-bn-D2bCvpik-unsplash.jpg mbot/saurabh-gill-38RthwbB3nE-unsplash.jpg").split()
MAIN = bool(environ.get('MAIN', None))
genius = Genius("api_key")
LOG_TEXT_P = """
ID - <code>{}</code>
Name - {}
"""
pre = []
@Mbot.on_message(filters.regex(r'https?://[^\s]+') & filters.incoming | filters.incoming  & filters.regex(r"spotify:"), group=1)
async def spotify_dl(Mbot,message: Message):
    if MAIN:
       await message.reply_text(f"Bot Is Under Maintenance ⚠️")
       return
    link = message.matches[0].group(0)
    if "https://www.deezer.com" in link:
       return
    if "https://youtu.be" in link:
          return await message.reply("301: Use @y2mate_api_bot Insted Of Me 🚫")
    try:
        parsed_item = await parse_spotify_url(link)
        item_type, item_id = parsed_item[0],parsed_item[1]
    except Exception as e:
        pass
        cr =  await message.reply("417: Not Critical, Retrying Again  🚫")
        await  Mbot.send_message(BUG,f" Private r: Unsupported [URI](link) Not critical {message.chat.id}  {message.from_user.id} {message.from_user.mention}")   
        try:
            link = head(link).headers['location']
            parsed_item = await parse_spotify_url(link)
            item_type, item_id = parsed_item[0],parsed_item[1]
        except Exception as e:
            pass 
            await  Mbot.send_message(BUG,f" Private r: Unsupported [URI](link) Failed twice {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
            return await cr.edit(f"501: This URI Is Not Supported ⚠")
    if message.text.startswith("/thumb"):
       try:
          await Mbot.send_message(BUG,f"Thumb download requested from {message.from_user.mention}")
          parsed_item = await parse_spotify_url(link)
          item_type, item_id = parsed_item[0],parsed_item[1]
          if item_type == "track":
             item = client.track(track_id=item_id)
             alb = client.album(album_id=item['album']['id'],)
             await message.reply_document(alb['images'][0]['url'])
          elif item_type == "playlist":
               play = client.playlist(playlist_id=item_id,)
               await message.reply_document(play['images'][0]['url'])
          elif item_type == "album":
               alb = client.album(album_id=item_id,)
               await message.reply_document(alb['images'][0]['url'])
          elif item_type == "artist":
               art = client.artist(item_id)
               await message.reply_document(art['images'][0]['url'])
       except Exception as e:
           pass
           await message.reply("404: sorry, thumbnail download is not available for this track 😔")
           await Mbot.send_message(BUG,f" thumb 400 {e}")
       return 
    if message.text.startswith("/preview"):
          parsed_item = await parse_spotify_url(link)
          item_type, item_id = parsed_item[0],parsed_item[1]
          if item_type == "track":
             try:
                 await Mbot.send_message(BUG,f"Preview download requested from {message.from_user.mention}")
                 item = client.track(track_id=item_id)
                 await  message.reply_audio(f"{item.get('preview_url')}")
             except Exception as e:
                 pass
                 await message.reply("404: sorry, audio preview is not available for this track 😔")
                 await Mbot.send_message(BUG,e)
          return 
    u = message.from_user.id
    randomdir = f"/tmp/{str(randint(1,100000000))}"
    mkdir(randomdir)
    try:
        m = await message.reply_text(f"⏳")
        await message.reply_chat_action(enums.ChatAction.TYPING)
    except ChatWriteForbidden:
        pass

    try:
        parsed_item = await parse_spotify_url(link)
        item_type, item_id = parsed_item[0],parsed_item[1]
        if item_type in ["show", "episode"]:
            items = await getIds(link)
            for item in items:
                cForChat = await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                sleeeps = await sleep (0.9)
                PForCopy = await message.reply_photo(item[5],caption=f"✔️ Episode Name : `{item[3]}`\n🕔 Duration : {item[4]//60}:{item[4]%60}")
                reply = await message.reply_text(f"sorry we removed support of  episode 😔 pls send other types album/playlist/track")
       
        elif item_type == "track":
            song = await fetch_spotify_track(client,item_id)
            #sleeeps = await sleep (0.9)
            try:
                item = client.track(track_id=item_id)
            except:
                pass
               
            try:
                if not item:
           #         await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)
                    PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n\n[IMAGE]({song.get('cover')})\nTrack id:`{song['deezer_id']}`")
           #         await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            #        document= await message.reply_document(song.get('cover'))  
                else:
                     PForCopy = await message.reply_photo(item['album']['images'][0]['url'],caption=f"🎧 Title : `{song['name']}­­`\n🎤 Artist : `{song['artist']}`­\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n❗️Is Local:`{item['is_local']}`\n 🌐ISRC: `{item['external_ids']['isrc']}`\n\n[IMAGE]({item['album']['images'][0]['url']})\nTrack id:`{song['deezer_id']}`",
                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
              #       document= await message.reply_document(alb['images'][0]['url'],
                #     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
              # await message.reply_audio(f"{item.get('preview_url')}")
            except:
                pass
         #       await message.reply_chat_action(enums.ChatAction.TYPING)
                PForCopy = await message.reply_text(f"🎧 Title : `{song['name']}`\n­🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n\n[IMAGE]({song.get('cover')})\ntrack id:`{song['deezer_id']}`")
       #     try:
       #         await message.reply_audio(f"{item.get('preview_url')}",
       #         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌", callback_data="cancel")]]))
      #      except:
      #          pass
      #      await sleep(0.6)
            try:
               path = await download_songs(item,randomdir)
            except Exception as e:
                pass
## optional you can clear this or add this by using #
                await message.reply(e)
          #      await Mbot.send_message(BUG,e)
                await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
         #       await message.reply_text(f"try `/saavn {song.get('name')} - {song.get('artist')}`")
            thumbnail = await thumb_down(item['album']['images'][0]['url'],song.get('deezer_id'))
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
                audio["DISCNUMBER"] =f" {item['disc_number']}"
                audio["TRACKNUMBER"] =f" {item['track_number']}"
                try:
                    audio["ISRC"] = item['external_ids']['isrc']
                except:
                    pass
                try:
                    songGenius = genius.search_song(song('name'), song('artist'))
                    audio["LYRICS"] = (songGenius.lyrics)
                except:
                    pass
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
            await copy(PForCopy,AForCopy)
        elif item_type == "playlist":
            play = client.playlist(playlist_id=item_id,)
           # if u in PREM:
            tracks = client.playlist_items(playlist_id=item_id,additional_types=['track'], offset=0, market=None)
          #  else:
         #        tracks = client.playlist_items(playlist_id=item_id,additional_types=['track'], limit=30, offset=0, market=None) 
            total_tracks = tracks.get('total')
            track_no = 1
            try:
                PForCopy = await message.reply_photo(play['images'][0]['url'],
                caption=f"▶️Playlist:{play['name']}\n📝Description:{play['description']}\n👤Owner:{play['owner']['display_name']}\n❤️Followers:{play['followers']['total']}\n🔢 Total Track:{play['tracks']['total']}\n\n[IMAGES]({play['images'][0]['url']})\n{play['uri']}")
          #      document= await message.reply_document(play['images'][0]['url'])
          #      sup = 40
           #     if u in PREM:
         #          re = 2
         #       else:
         #            re = play['tracks']['total']
          #      if re > sup:
          #         await message.reply(f"trying to send first 40 tracks of {play['name']} total {re}")     
            except Exception as e:
                pass
                PForCopy = await message.reply(f"▶️Playlist:{play['name']}\n📝Description:{play['description']}\n👤Owner:{play['owner']['display_name']}\n❤️Followers:{play['followers']['total']}\n🔢 Total Track:{play['tracks']['total']}\n\n[IMAGES]({play['images'][0]['url']})\n{play['tracks']['uri']}")
                await message.reply("are you sure it's a valid playlist 🤨?")
            
            for track in tracks['items']:
                song = await fetch_spotify_track(client,track.get('track').get('id'))
                item = client.track(track_id=track['track']['id'])
             #   cForChat = await message.reply_chat_action(enums.ChatAction.TYPING)
               #sleeeps = await sleep (0.6)
            #    try:
           #        PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n❗️Is Local: `{track['is_local']}`\n🔢 Track No: `{track_no}`\n🔢 Total Track: `{total_tracks}`\n\n[IMAGE]({song.get('cover')})\ntrack id:`{song['deezer_id']}`")
            #       document= await message.reply_document(song.get('cover'))
             #   except:
              #      pass
                  #  PForCopy = await message.reply_text(f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🗓 Release Year: `{song['year']}`\n\n[IMAGE]({song.get('cover')})\ntrack id:`{song['deezer_id']}`")
                #PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🎼 Genre : `{song['genre']}`\n🗓 Release Year: `{song['year']}`\n🔢 Track No: `{song['playlist_num']}`\n🔢 Total Track: `{total_tracks}`\n\n[IMAGE]({song.get('cover')})\ntrack id:`{song['deezer_id']}")
                await sleep(0.6)
                try:
                   path = await download_songs(item,randomdir)
                except Exception as e:
                    pass
## optional you can clear this or add this by using #
                    await message.reply(e)
                    await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
            #        await message.reply_text(f"try `/saavn {song.get('name')} - {song.get('artist')}`")
            #        await message.reply(f"[Click Here](https://t.me/)")
                thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                await sleep(0.6)
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
                    audio["discnumber"] =f" {item['disc_number']}"
                    audio["tracknumber"] =f" {item['track_number']}"
                    try:
                        audio["ISRC"] = item['external_ids']['isrc']
                    except:
                        pass
                    try:
                       songGenius = genius.search_song(song('name'), song('artist'))
                       audio["LYRICS"] = (songGenius.lyrics)
                    except:
                        pass
                except:
                     pass
                audio.save()
                try:
                   audio = MP3(path, ID3=ID3)
                   audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnail,'rb').read()))
                except Exception as e:
                    pass
                audio.save()
                try:
                    AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,parse_mode=enums.ParseMode.MARKDOWN,quote=True)  
                except:
                  pass
                #AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,parse_mode=enums.ParseMode.MARKDOWN,quote=True)
                await copy(PForCopy,AForCopy)
                #feedback = await message.reply_text(f"Done✅",   
                 #reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Feedback", callback_data="feed")]]))
               # shutil.rmtree(randomdir)
                track_no += 1
           
        elif item_type == "album":
            alb = client.album(album_id=item_id,)
            try:
                PForCopy = await message.reply_photo(alb['images'][0]['url'],
                caption=f"💽Album: {alb['name']}\n👥Artists: {alb['artists'][0]['name']}\n🎧Total tracks{alb['total_tracks']}\n🗂Category: {alb['album_type']}\n📆Published on: {alb['release_date']}\n\n[IMAGE]({alb['images'][0]['url']})\n{alb['uri']}")
           #     await message.reply_document(alb['images'][0]['url'])
            except Exception as e:
                pass
                err = print(e)
                PForCopy = await message.reply(f"💽Album: {alb['name']}\n👥Artists: {alb['artists'][0]['name']}\n🎧Total tracks{alb['total_tracks']}\n🗂Category: {alb['album_type']}\n📆Published on: {alb['release_date']}\n\n[IMAGE]({alb['images'][0]['url']})\n{alb['uri']}")
           # if u in PREM:
            tracks = client.album_tracks(album_id=item_id, offset=0, market=None)
          #  else:
          #       tracks = client.album_tracks(album_id=item_id, limit=30, offset=0, market=None)

            for track in tracks['items']:
                item = client.track(track_id=track['id'])
                song = await fetch_spotify_track(client,track.get('id'))
              #  cForChat = await message.reply_chat_action(enums.ChatAction.TYPING)
                sleeeps = await sleep (0.6)
                try:
                   path = await download_songs(item,randomdir)
                except Exception as e:
                    pass
## optional you can clear this or add this by using #
                    await message.reply(e)
                    await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
             #       await message.reply_text(f"try `/saavn {song.get('name')} - {song.get('artist')}`")
            #        await message.reply(f"[Click Here](https://t.me/)")
               # path = await download_songs(item,randomdir)
                thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                await sleep(0.6)
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
                    audio["discnumber"] =f" {item['disc_number']}"
                    audio["tracknumber"] =f" {item['track_number']}"
                    try:
                        audio["ISRC"] =f" {item['external_ids']['isrc']}"
                    except:
                        pass
                    try:
                        songGenius = genius.search_song(song('name'), song('artist'))
                        audio["LYRICS"] = (songGenius.lyrics)
                    except:
                       pass
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
                if not path:
                           await message.reply_text(f"⚠️")
                else:
                    AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail,parse_mode=enums.ParseMode.MARKDOWN,quote=True)
                await copy(PForCopy,AForCopy)
           
        elif item_type == "artist":
             art = client.artist(item_id)
             try:
                 PForCopy = await message.reply_photo(art['images'][0]['url'],
                 caption=f"👤Artist: **{art['name']}­**\n❤️Followers:{art['followers']['total']}­\n🎶Generes:{art['genres']}­\n🗂Category:{art['type']}­\n❤️Popularity:{art['popularity']}­\n\n[IMAGE]({art['images'][0]['url']})\nArtist id:`{art['id']}`")
              #   await message.reply_document(art['images'][0]['url'])
             except Exception as e:
                 pass
                 await message.reply(f"👤Artist: **{art['name']}­**\n❤️Followers:{art['followers']['total']}­\n🎶Generes:{art['genres']}­\n🗂Category:{art['type']}­\n❤️Popularity:{art['popularity']}­\n\n[IMAGE]({art['images'][0]['url']})\nArtist id:`{art['id']}`")     
             
           #  if u in PREM:
          #      tracks = client.artist_albums(artist_id=item_id)
             #else:
             await message.reply(f"Sending Top 10 tracks of {art['name']}")
             tracks = client.artist_top_tracks(artist_id=item_id,)
             for item in tracks['tracks'][:10]:
                 song = await fetch_spotify_track(client,item.get('id'))
                 track = client.track(track_id=item['id'])
                 track_no = 1
                 await sleep(0.6)
                 try:
                     path = await download_songs(item,randomdir)
                 except Exception as e:
                     pass
## optional you can clear this or add this by using #
                     await message.reply(e)
                     await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
            #         await message.reply_text(f"try `/saavn {song.get('name')} - {song.get('artist')}`")
            #         await message.reply(f"[Click Here](https://t.me/)")
                 thumbnail = await thumb_down(song.get('cover'),song.get('deezer_id'))
                 audio = EasyID3(path)
                 try:
                     audio["TITLE"] = f" {song.get('name')}"
                     audio["originaldate"] = song.get('year')
              #       audio["YEAR_OF_RELEASE"] = song.get('year')
                     audio["WEBSITE"] = "https://t.me/Spotify_downloa_bot"
                #     audio["GEEK_SCORE"] = "9"
                     audio["ARTIST"] = art.get('name')                                                                            
                     audio["ALBUM"] = song.get('album')
                     audio["DATE"] = song.get('year')
                     audio["discnumber"] =f" {track['disc_number']}"
                     audio["tracknumber"] =f" {track['track_number']}"
                     try:
                         audio["ISRC"] =f" {track['external_ids']['isrc']}"
                     except:
                         pass
                     try:
                        songGenius = genius.search_song(song('name'), song('artist'))
                        audio["LYRICS"] = (songGenius.lyrics)
                     except:
                         pass
                 except:
                     pass
                 audio.save()
                 try:
                   audio = MP3(path, ID3=ID3)
                   audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open(thumbnail,'rb').read()))
                 except Exception as e:
                   pass
                  # print(e)
                 audio.save()
                 AForCopy = await message.reply_audio(path,performer=f"{song.get('artist')}­",title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail, parse_mode=enums.ParseMode.MARKDOWN,quote=True)
                 await copy(PForCopy,AForCopy)
    except MissingSchema:
        pass
        await message.reply("are you sure it's a valid song 🤨?")
    except RPCError:
        pass
        await message.reply(f"telegram says 500 error,so please try again later.❣️")
    except ChatWriteForbidden:
        pass
        chat=message.chat.id
        try:
            await Mbot.leave_chat(chat)
            k = await Mbot.send_message(-1001744816254,f"{chat} {message.chat.username} or {message.from_user.id}")
            await  k.pin()
            sp = f"I have left from {chat} reason: I Am Not  Admin "
            await Mbot.send_message(message.from_user.id,f"{sp}")
        except:
            pass
    except UserIsBlocked:
        pass
        K = await  Mbot.send_message(BUG,f" private {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
        k.pin()
    except IOError:
        pass
        K = await  Mbot.send_message(BUG,f" Private r: socket {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
        k.pin()
    except (FileNotFoundError, OSError):
        pass
        await message.reply('Sorry, We Are Unable To Procced It 🤕❣️')
    except BrokenPipeError:
        pass
        K = await  Mbot.send_message(BUG,f" private r: broken {message.chat.id}  {message.from_user.id} {message.from_user.mention}")
    except Forbidden:
       T = await message.reply_text(f"Dude check weather I have enough rights😎⚠️")
    except UnboundLocalError:
       pass
  #     T = await message.reply_text(f"[{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) Track Not Found ⚠️")
        
    except FloodWait as e:
        pass
        await sleep(e.value)
        await message.reply_text(f"Telegram says: [420 FLOOD_WAIT_X] - A wait of {e.value} seconds is required !")
    except IOError as e:
        pass
        K = await  Mbot.send_message(BUG,f" private r: broken {message.chat.id} {message.from_user.mention}")
           
    except Exception as e:
        pass
        LOGGER.error(e)
        await m.edit(e)
        await Mbot.send_message(BUG,f" Finnal {e}")
      #  K = await message.reply_text(f"private [{song.get('name')} - {song.get('artist')}](https://open.spotify.com/track/{song.get('deezer_id')}) failed to send error: {e}")
     #   H = await message.reply_text(f"Done✅",   
     #        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Error Detected", callback_data="bug")]]))
    #    await message.reply_text(f"try: `/saavn {song.get('name')}`")
        await message.reply('400: Sorry, We Are Unable To Procced It 🤕❣️')
    finally:
        await sleep(2.0)
        try:
            rmtree(randomdir)
        except:
            pass
        try:
            await message.reply_text(f"Done✅",   
         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Feedback", callback_data="feed")]]))
            await message.reply_text(f"Check out @spotify_downloa(music)  @spotifynewss(News)")
            await m.delete()
        except:
            pass 
       # await message.reply_text(f"thumbnail and details is temp removed due to  there is  something going on telegram side:)")
           
@Mbot.on_callback_query(filters.regex(r"feed"))
async def feedback(Mbot,query):
      try:
          K = await query.message.edit(f"Feedback 🏴‍☠️",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Press here", url="https://t.me/dailychannelsbot?start=spotify_downloa_bot")]]))
          H = print("New Feedback")
          if BUG:
             await copy(K,H)
      except Exception as e:
          pass
         
@Mbot.on_callback_query(filters.regex(r"bug"))                                                                                                          
async def bug(_,query):
      try:                                                                                                                                  
          K = await query.message.edit(f'please report to the dev say "private version" with above  error occurred message')
          await sleep(2.3)
          H = await query.message.edit(f"Bug Report 🪲",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Report to dev ", url="https://t.me/masterolic")]]))
          if BUG:
             await copy(K,H)
      except Exception as e:
          pass
          print(e)

@Mbot.on_callback_query(filters.regex(r"cancel"))                                                                                                          
async def bug(_,query):
          await sleep(0.2)
          await query.message.delete()
          await query.answer("closed❌")
