from pyrogram import Client, filters
from bot import LOG_GROUP
import aiohttp
import os,pathlib,shutil,glob
from random import randint
import youtube_dl
from youtube_dl import YoutubeDL
#from .helpers import playlisthelper


def audio_opt(path):
    audio_opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        'noplaylist': True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
        "outtmpl": f"{path}/%(title)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    return audio_opts

def ydl_data(opts, url):
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url,download=False)
            return ytdl_data
    except Exception as e:
        return e

async def ytdl_down(opts, url,randomdir):
    with youtube_dl.YoutubeDL(opts) as ydl:
        a = ydl.download([url])
        files = glob.glob(f'{randomdir}/**/*.mp3', recursive=True)
        return files


@Client.on_message(filters.regex(r'https?://.*you[^\s]+') & filters.private)
async def link_handler(client, message):
    link = message.matches[0].group(0)
    try:
        if "playlist" not in link:
            ytdl_data = ydl_data(audio_opt("."), link)
            try:
                performer = ytdl_data['artist']
            except:
                performer = ytdl_data['uploader']
            forcopydata = await message.reply_photo(photo=f"https://i.ytimg.com/vi/{ytdl_data['id']}/hqdefault.jpg",caption=f"🎧 Title : `{ytdl_data['title']}`\n🎤 Artist : `{performer}`")
            randomdir = "/tmp/"+str(randint(1,100000000))
            os.mkdir(randomdir)
            files = await ytdl_down(audio_opt(randomdir),link,randomdir)
            thumbnails = list(glob.glob(f'{randomdir}/**/*.webp', recursive=True))
            #print(files[0],thumbnails[0])
            try:
                thumbnail = thumbnails[0]
            except:
                thumbnail = None
            forcopyaudio = await message.reply_audio(audio=files[0],thumb=thumbnail,performer=performer,duration=ytdl_data['duration'])
            if LOG_GROUP is not None:
                await forcopydata.copy(LOG_GROUP)
                await forcopyaudio.copy(LOG_GROUP)
            shutil.rmtree(randomdir)
        else:
            await message.reply_photo(photo="https://telegra.ph/file/6f228f684d55821363e36.jpg")
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
        shutil.rmtree(randomdir)
