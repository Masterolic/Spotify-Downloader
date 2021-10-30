from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from bot import LOG_GROUP,UPDATES_CHANNEL
from ..helpers.force_sub_handler import handle_force_sub
import os,pathlib,shutil,deezer,wget
from random import randint
from ..helpers.deezerhelper import parse_deezer_url,fetch_tracks,download_now,artist_data


class ReplyKeyboard(ReplyKeyboardMarkup):
    def __init__(self, resize_keyboard=None, one_time_keyboard=None,
                 selective=None, row_width=3):
        self.keyboard = list()
        super().__init__(
            keyboard=self.keyboard,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective
        )
        self.row_width = row_width

    def add(self, *args):
        self.keyboard = [
            args[i:i + self.row_width]
            for i in range(0, len(args), self.row_width)
        ]

    def row(self, *args):
        self.keyboard.append([button for button in args])

@Client.on_message(filters.regex(r'https?://.*deezer[^\s]+') & filters.private)
async def link_handler(client, message):
    if UPDATES_CHANNEL is not None:
        back = await handle_force_sub(client, message)
        if back == 400:
            return
    link = message.matches[0].group(0)
    client = deezer.Client()
    try:
        itemss = parse_deezer_url(link)
        item_type = itemss[0]
        item_id = itemss[1]
        songs = fetch_tracks(client,item_type,item_id)
        if item_type == "playlist" or item_type == "album" or item_type == "track":
            for song in songs:
                forcopydata = await message.reply_photo(photo=song['cover'],caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n🎤 Album : `{song['album']}`\n🎤 Song Number : `{song['playlist_num']}`")
                performer = song['artist']
                randomdir = "/tmp/"+str(randint(1,100000000))
                os.mkdir(randomdir)
                files = download_now(client,f"https://www.deezer.com/us/track/{song['deezer_id']}","/tmp")
                thumbname = wget.download(song['cover'])
                forcopyaudio = await message.reply_audio(audio=files[0],performer=performer,thumb=thumbname)
                if LOG_GROUP is not None:
                    await forcopydata.copy(LOG_GROUP)
                    await forcopyaudio.copy(LOG_GROUP)
                shutil.rmtree(randomdir)
                os.remove(thumbname)
        elif item_type == "artist":
            await message.reply("This Is An Artist Account Link. Send me Track, Playlist or Album Link :)")
        else:
            await message.reply_photo(photo="https://telegra.ph/file/6f228f684d55821363e36.jpg")
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
