from pyrogram import Client, filters
import aiohttp,spotipy,re
from bot import LOG_GROUP,UPDATES_CHANNEL
from bot.helpers import spotify
from spotify_dl import spotify_dl
from ..helpers.force_sub_handler import handle_force_sub
from bot import SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET
from spotipy.oauth2 import SpotifyClientCredentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET))


@Client.on_message(filters.regex(r'https?://open.spotify.com[^\s]+') & filters.private)
async def link_handler(client, message):
    if UPDATES_CHANNEL is not None:
        back = await handle_force_sub(client, message)
        if back == 400:
            return
    link = url = re.search("(?P<url>https?://[^\s]+)", message.text).group("url")
    try:
        if spotify.parse_spotify_url(link)=="track":
            track = spotify.fetch_tracks(sp,"track",link)
            forcopydata = await message.reply_photo(photo=track[0]["cover"],caption=f"🎧 Title : `{track[0]['name']}`\n🎤 Artist : `{track[0]['artist']}`\n📚 Album: `{track[0]['album']}`\n💽 Genre : `{track[0]['genre']}`")
            forcopyaudio = await message.reply_audio(audio=spotify.download_song(track,"/tmp"))
            if LOG_GROUP is not None:
                await forcopydata.copy(LOG_GROUP)
                await forcopyaudio.copy(LOG_GROUP)
        elif spotify.parse_spotify_url(link)=="playlist":
            tracks = spotify.fetch_tracks(sp,"playlist",link)
            for track in tracks:
                forcopydata = await message.reply_photo(photo=track["cover"],caption=f"🎧 Title : `{track['name']}`\n🎤 Artist : `{track['artist']}`\n📚 Album: `{track['album']}`\n💽 Genre : `{track['genre']}`")
                forcopyaudio = await message.reply_audio(audio=spotify.download_songs(track,"/tmp"))
                if LOG_GROUP is not None:
                    await forcopydata.copy(LOG_GROUP)
                    await forcopyaudio.copy(LOG_GROUP)
        elif spotify.parse_spotify_url(link)=="album":
            tracks = spotify.fetch_tracks(sp,"album",link)
            for track in tracks:
                forcopydata = await message.reply_photo(photo=track["cover"],caption=f"🎧 Title : `{track['name']}`\n🎤 Artist : `{track['artist']}`\n📚 Album: `{track['album']}`\n💽 Track No : `{track['playlist_num']}`\n💽 Total Track : `{track['num_tracks']}`\n💽 Genre : `{track['genre']}`")
                forcopyaudio = await message.reply_audio(audio=spotify.download_songs(track,"/tmp"))
                if LOG_GROUP is not None:
                    await forcopydata.copy(LOG_GROUP)
                    await forcopyaudio.copy(LOG_GROUP)

        else:
            await message.reply_audio(audio=spotify_dl.spotify_dl(link,output="/tmp"))
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)
