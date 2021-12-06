from pyrogram import Client, filters
from bot import LOG_GROUP,UPDATES_CHANNEL,AUTH_CHATS
import os,pathlib,shutil,glob,re,requests,wget
from random import randint
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
from ..helpers.force_sub_handler import handle_force_sub


def getPlaylistLinks(url: str) -> map:
    page_text = requests.get(url).text
    parser = re.compile(r"watch\?v=\S+?list=")
    playlist = set(re.findall(parser, page_text))
    playlist = map(
        (lambda x: "https://www.youtube.com/" + x.replace("\\u0026list=", "")), playlist
    )
    return playlist


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
    if UPDATES_CHANNEL is not None:
        back = await handle_force_sub(client, message)
        if back == 400:
            return
    link = message.matches[0].group(0)
    try:
        if "playlist" in link:
            playlisturls = getPlaylistLinks(link)
            for listurl in playlisturls:
                ytdl_data = ydl_data(audio_opt("."), listurl)
                try:
                    performer = ytdl_data['artist']
                except:
                    performer = ytdl_data['uploader']
                forcopydata = await message.reply_photo(photo=f"https://i.ytimg.com/vi/{ytdl_data['id']}/hqdefault.jpg",caption=f"🎧 Title : `{ytdl_data['title']}`\n🎤 Artist : `{performer}`")
                randomdir = "/tmp/"+str(randint(1,100000000))
                os.mkdir(randomdir)
                files = await ytdl_down(audio_opt(randomdir),listurl,randomdir)
                thumbnail = wget.download(f"https://i.ytimg.com/vi/{ytdl_data['id']}/hqdefault.jpg")
                forcopyaudio = await message.reply_audio(audio=files[0],thumb=thumbnail,performer=performer,duration=ytdl_data['duration'])
                if LOG_GROUP is not None:
                    await forcopydata.copy(LOG_GROUP)
                    await forcopyaudio.copy(LOG_GROUP)
                shutil.rmtree(randomdir)
            return


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
            thumbnail = wget.download(f"https://i.ytimg.com/vi/{ytdl_data['id']}/sddefault.jpg")
            forcopyaudio = await message.reply_audio(audio=files[0],thumb=thumbnail,performer=performer,duration=ytdl_data['duration'])
            if LOG_GROUP is not None:
                await forcopydata.copy(LOG_GROUP)
                await forcopyaudio.copy(LOG_GROUP)
            shutil.rmtree(randomdir)
        
        else:
            await message.reply_text("Please use a valid link. (Channel link not supported)")
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
        shutil.rmtree(randomdir)

@Client.on_message(filters.command('yta') & filters.group & filters.chat(AUTH_CHATS))
async def yta_handler(client, message):
    try:
        if UPDATES_CHANNEL is not None:
            back = await handle_force_sub(client, message)
            if back == 400:
                return
    except:
        pass
    try:
        link = message.matches[0].group(0)
        if "playlist" in link:
            playlisturls = getPlaylistLinks(link)
            for listurl in playlisturls:
                ytdl_data = ydl_data(audio_opt("."), listurl)
                try:
                    performer = ytdl_data['artist']
                except:
                    performer = ytdl_data['uploader']
                forcopydata = await message.reply_photo(photo=f"https://i.ytimg.com/vi/{ytdl_data['id']}/hqdefault.jpg",caption=f"🎧 Title : `{ytdl_data['title']}`\n🎤 Artist : `{performer}`")
                randomdir = "/tmp/"+str(randint(1,100000000))
                os.mkdir(randomdir)
                files = await ytdl_down(audio_opt(randomdir),listurl,randomdir)
                thumbnail = wget.download(f"https://i.ytimg.com/vi/{ytdl_data['id']}/hqdefault.jpg")
                forcopyaudio = await message.reply_audio(audio=files[0],thumb=thumbnail,performer=performer,duration=ytdl_data['duration'])
                if LOG_GROUP is not None:
                    await forcopydata.copy(LOG_GROUP)
                    await forcopyaudio.copy(LOG_GROUP)
                shutil.rmtree(randomdir)
            return


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
            thumbnail = wget.download(f"https://i.ytimg.com/vi/{ytdl_data['id']}/sddefault.jpg")
            forcopyaudio = await message.reply_audio(audio=files[0],thumb=thumbnail,performer=performer,duration=ytdl_data['duration'])
            if LOG_GROUP is not None:
                await forcopydata.copy(LOG_GROUP)
                await forcopyaudio.copy(LOG_GROUP)
            shutil.rmtree(randomdir)
        
        else:
            await message.reply_text("Please use a valid link. (Channel link not supported)")
    except TypeError:
        await message.reply_text("/yta [link]")
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)