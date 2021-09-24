from bot import LOG_GROUP
from pyrogram import Client, filters
import requests,shutil,os,wget
from random import randint
from .youtubemusic import ytdl_down

def audio_opt(title,path):
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
        "outtmpl": f"{path}/{title}.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    return audio_opts

api_base = "https://jiosaavnapi.up.railway.app/"

@Client.on_message(filters.regex(r'https?://.*jiosaavn[^\s]+') & filters.private)
async def link_handler(client, message):
    link = message.matches[0].group(0)
    data = requests.get(f"{api_base}song/?query={link}").json()
    forcopydata = await message.reply_photo(photo=data['image'],caption=f"🎧 Title : `{data['song']}`\n📚 Album : `{data['album']}`\n🎤 Artist : `{data['primary_artists']}`\n🎤 Language : `{data['language']}`\n{data['copyright_text']}")
    randomdir = "/tmp/"+str(randint(1,100000000))
    os.mkdir(randomdir)
    files = await ytdl_down(audio_opt(f"{data['song']} - {data['album']}",randomdir),data['media_url'],randomdir)
    thumbname = wget.download(data['image'])
    forcopyaudio = await message.reply_audio(audio=files[0],thumb=thumbname,performer=data['primary_artists'])
    if LOG_GROUP is not None:
        await forcopydata.copy(LOG_GROUP)
        await forcopyaudio.copy(LOG_GROUP)
    shutil.rmtree(randomdir)
    os.remove(thumbname)
