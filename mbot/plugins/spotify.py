"""MIT License

Copyright (c) 2022 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from mbot import AUTH_CHATS, LOGGER, Mbot,LOG_GROUP
from pyrogram import filters
from mbot.utils.mainhelper import parse_spotify_url,fetch_spotify_track,download_songs,thumb_down,copy
from mbot.utils.ytdl import getIds,ytdl_down,audio_opt
import spotipy
from os import mkdir
from random import randint

client = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials())

@Mbot.on_message(filters.regex(r'https?://open.spotify.com[^\s]+') & filters.private | filters.regex(r'https?://open.spotify.com[^\s]+') & filters.command(["spotify","spotdl"]) | filters.private & filters.regex(r"spotify:") & filters.chat(AUTH_CHATS))
async def spotify_dl(_,message):
    link = message.matches[0].group(0)
    m = await message.reply_text(f"**Gathering info from your [link]({link}).**")
    try:
        parsed_item = await parse_spotify_url(link)
        item_type, item_id = parsed_item[0],parsed_item[1]
        randomdir = "/tmp/"+str(randint(1,100000000))
        mkdir(randomdir)
        if item_type in ["show", "episode"]:
            items = await getIds(link)
            for item in items:
                PForCopy = await message.reply_photo(item[5],caption=f"✔️ Episode Name : `{item[3]}`\n🕔 Duration : {item[4]//60}:{item[4]%60}")
                fileLink = await ytdl_down(audio_opt(randomdir,item[2]),f"https://open.spotify.com/episode/{item[0]}")
                thumbnail = await thumb_down(item[5],item[0])
                AForCopy = await message.reply_audio(fileLink,title=item[3].replace("_"," "),performer="Spotify",duration=int(item[4]),caption=f"[{item[3]}](https://open.spotify.com/episode/{item[0]})",thumb=thumbnail)
                if LOG_GROUP:
                    await copy(PForCopy,AForCopy)
            return await m.delete()
        elif item_type == "track":
            song = await fetch_spotify_track(client,item_id)
            PForCopy = await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🎼 Genre : `{song['genre']}`\n🗓 Release Year: `{song['year']}`")
            path = await download_songs(song,randomdir)
            thumbnail = await thumb_down(song.get('cover'),song.get('name'))
            AForCopy = await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail)
            if LOG_GROUP:
                await copy(PForCopy,AForCopy)
            return await m.delete()
        elif item_type == "playlist":
            tracks = client.playlist_items(playlist_id=item_id,additional_types=['track'])
            total_tracks = tracks.get('total')
            for track in tracks['items']:
                song = await fetch_spotify_track(client,track.get('track').get('id'))
                await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🎼 Genre : `{song['genre']}`\n🗓 Release Year: `{song['year']}`\n🔢 Track No: `{song['playlist_num']}`\n🔢 Total Track: `{total_tracks}`")
                path = await download_songs(song,randomdir)
                thumbnail = await thumb_down(song.get('cover'),song.get('name'))
                await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail)
                if LOG_GROUP:
                    await copy(PForCopy,AForCopy)
            return await m.delete()
        elif item_type == "album":
            tracks = client.album_tracks(album_id=item_id)
            for track in tracks['items']:
                song = await fetch_spotify_track(client,track.get('id'))
                await message.reply_photo(song.get('cover'),caption=f"🎧 Title : `{song['name']}`\n🎤 Artist : `{song['artist']}`\n💽 Album : `{song['album']}`\n🎼 Genre : `{song['genre']}`\n🗓 Release Year: `{song['year']}`")
                path = await download_songs(song,randomdir)
                thumbnail = await thumb_down(song.get('cover'),song.get('name'))
                await message.reply_audio(path,performer=song.get('artist'),title=f"{song.get('name')} - {song.get('artist')}",caption=f"[{song.get('name')}](https://open.spotify.com/track/{song.get('deezer_id')}) | {song.get('album')} - {song.get('artist')}",thumb=thumbnail)
                if LOG_GROUP:
                    await copy(PForCopy,AForCopy)
            return await m.delete()
    except Exception as e:
        LOGGER.error(e)
        await m.edit_text(e)