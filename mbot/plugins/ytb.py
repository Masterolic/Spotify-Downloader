from pyrogram import filters, Client as Mbot
from os import mkdir,environ 
from random import randint
from mbot import BUG as  LOG_GROUP , LOG_GROUP as DUMP_GROUP
from pyrogram import filters
from shutil import rmtree 
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from requests import get
import traceback,os
FIXIE_SOCKS_HOST= environ.get('FIXIE_SOCKS_HOST')
async def thumb_down(videoId):
    with open(f"/tmp/{videoId}.jpg","wb") as file:
        file.write(get(f"https://img.youtube.com/vi/{videoId}/default.jpg").content)
    return f"/tmp/{videoId}.jpg"
async def ytdl_video(path, video_url, id):
    print(video_url)
    qa = "mp4"  # Set to MP4 format
    file = f"{path}/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": file,
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "cache-dir": "/tmp/",
        "nocheckcertificate": True,
 #       "proxy": f"socks5://{FIXIE_SOCKS_HOST}",
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            print(filename)
            return filename
        except (IOError, BrokenPipeError):
            pass
            video = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(video)
            print(filename)
            return filename
        except Exception as e:
                ydl_opts = {
               'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
               'default_search': 'ytsearch',
               'noplaylist': True,
               "nocheckcertificate": True,
               "outtmpl": file,
               "quiet": True,
               "addmetadata": True,
               "prefer_ffmpeg": True,
               "geo_bypass": True,
               "cache-dir": "/tmp/",
               "nocheckcertificate": True,
               "proxy": f"socks5://{FIXIE_SOCKS_HOST}"
    }
                with YoutubeDL(ydl_opts) as ydl:
                   try:
                       video = ydl.extract_info(video_url, download=True)
                       filename = ydl.prepare_filename(video)
                       print(filename)
                       return filename
                   except Exception as e:
                       print(e)

async def ytdl_down(path,video_url,id):
#    pool = multiprocessing.Pool(processes=8)
    print(video_url)
    qa="mp3"
    query = f"{video_url[3]} - {video_url[2]}".replace(":", "").replace("\"", "")
    file = f"{path}/{query}"
#    arts=",".join(ur['name'] for ur in item['artists'][0:2])
    results = YoutubeSearch(f"{query}", max_results=1).to_dict()
    video_url = f"https://www.youtube.com/watch?v={results[0]['id']}"
    ydl_opts = {
        'format': "bestaudio",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": file,
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "cache-dir": "/tmp/",
        "nocheckcertificate": True,
        "postprocessors": [{'key': 'FFmpegExtractAudio', 'preferredcodec': qa, 'preferredquality': '693'}],
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(video_url,download=True)
           # info = ydl.extract_info(video)
        #    filename = ydl.prepare_filename(video)
            return f"{file}.{qa}"
        except (IOError,BrokenPipeError):
            pass
            video = ydl.extract_info(video_url, download=True)
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(video)
            print(filename)
            return f"{filename}.{qa}"
        except Exception as e:
          if FIXIE_SOCKS_HOST:
            try:
                ydl_opts = {
                'format': "bestaudio",
                'default_search': 'ytsearch',
                'noplaylist': True,
                "nocheckcertificate": True,
                "outtmpl": file,
                "quiet": True,
                "addmetadata": True,
                "prefer_ffmpeg": True,
                "geo_bypass": True,
                "cache-dir": "/tmp/",
                "nocheckcertificate": True,
                "proxy": f"socks5://{FIXIE_SOCKS_HOST}",
                "postprocessors": [{'key': 'FFmpegExtractAudio', 'preferredcodec': qa, 'preferredquality': '693'}],
                }
                with YoutubeDL(ydl_opts) as ydl:
                    video = ydl.extract_info(video_url,download=True)
                    return f"{file}.{qa}"
            except Exception as e:
                print(e)
async def getIds(video):
    ids = []
    with YoutubeDL({'quiet':True}) as ydl:
        info_dict = ydl.extract_info(video, download=False)
        try:
            info_dict = info_dict['entries']
            ids.extend([x.get('id'),x.get('playlist_index'),x.get('creator') or x.get('uploader'),x.get('title'),x.get('duration'),x.get('thumbnail')] for x in info_dict)
        except:
            ids.append([info_dict.get('id'),info_dict.get('playlist_index'),info_dict.get('creator') or info_dict.get('uploader'),info_dict.get('title'),info_dict.get('duration'),info_dict.get('thumbnail')])
    return ids
@Mbot.on_message(filters.regex(r'https?://.*youtube[^\s]+') & filters.incoming|filters.regex(r'(https?:\/\/(?:www\.)?youtu\.?be(?:\.com)?\/.*)') & filters.incoming)
async def _(Mbot,message):
    try:
        m = await message.reply_sticker("CAACAgIAAxkBATWhF2Qz1Y-FKIKqlw88oYgN8N82FtC8AAJnAAPb234AAT3fFO9hR5GfHgQ")
    except:
        pass
    link = message.matches[0].group(0)
    if "channel" in link or "/c/" in link:
        return await m.edit_text("**Channel** Download Not Available. ")
    if "shorts" in link:
        try:
            randomdir = "/tmp/"+str(randint(1,100000000))
            mkdir(randomdir)
            fileLink = await  ytdl_video(randomdir,link, message.from_user.id)
            AForCopy=await message.reply_video(fileLink)
            if os.path.exists(randomdir):
               rmtree(randomdir)
            await m.delete()
            if DUMP_GROUP:
                await AForCopy.copy(DUMP_GROUP)
        except Exception as e:
            await m.delete()
            if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"YouTube Shorts {e} {link}")
               await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @masterolic or support chat @spotify_supportbot 🤖  ")
               print(traceback.format_exc())
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())
               
        return await message.reply("Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
    try:
        ids = await getIds(message.matches[0].group(0))
        videoInPlaylist = len(ids)
        randomdir = "/tmp/"+str(randint(1,100000000))
        mkdir(randomdir)
        for id in ids:
  #          await message.reply(id)
  #          await message.reply(id[2])
            PForCopy = await message.reply_photo(f"https://i.ytimg.com/vi/{id[0]}/hqdefault.jpg",caption=f"🎧 Title : `{id[3]}`\n🎤 Artist : `{id[2]}`\n💽 Track No : `{id[1]}`\n💽 Total Track : `{videoInPlaylist}`")
            fileLink = await  ytdl_down(randomdir,id, message.from_user.id)
            print("down completely")
            thumnail = await thumb_down(id[0])
          #  await message.reply(fileLink)
        #    await message.reply_audio(fileLink)
            AForCopy = await message.reply_audio(fileLink,caption=f"[{id[3]}](https://youtu.be/{id[0]}) - {id[2]} Thank you for using - @InstaReelsdownbot",title=id[3].replace("_"," "),performer=id[2],thumb=thumnail,duration=id[4])
            if DUMP_GROUP:
                await PForCopy.copy(DUMP_GROUP)
                await AForCopy.copy(DUMP_GROUP)
        await m.delete()
        if os.path.exists(randomdir):
           rmtree(randomdir)
        await message.reply("Check out @spotify_downloa_bot(music)  @spotifynewss(Channel) \n Please Support Us By /donate To Maintain This Project")
    except Exception as e:
        print(e)
        if LOG_GROUP:
               await Mbot.send_message(LOG_GROUP,f"Youtube {e} {link}")
               await message.reply(f"400: Sorry, Unable To Find It  try another or report it  to @masterolic or support chat @spotify_supportbot 🤖  ")
               await Mbot.send_message(LOG_GROUP, traceback.format_exc())
