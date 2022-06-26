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
from random import randint 
#from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from mbot import LOGGER,LOG_GROUP
from requests import get
from asgiref.sync import sync_to_async
BUG = "" #add your bug log group id here eg "-100174481625"
@sync_to_async
def parse_deezer_url(url):
    url = get(url).url
    parsed_url = url.replace("https://www.deezer.com/", "")
    item_type = parsed_url.split("/")[1]
    item_id = parsed_url.split("/")[2].split("?")[0]
    return item_type, item_id

@sync_to_async
def parse_spotify_url(url):
    if url.startswith("spotify"):
        return url.split(":")[1]
    url = get(url).url
    parsed_url = url.replace("https://open.spotify.com/", "").split("/")
    return parsed_url[0],parsed_url[1].split("?")[0]

@sync_to_async
def thumb_down(link,deezer_id):
    with open(f"/tmp/thumbnails/{deezer_id}.jpg","wb") as file:
        file.write(get(link).content)
    return f"/tmp/thumbnails/{deezer_id}.jpg"

@sync_to_async
def fetch_tracks(dz, item_type, item_id):
    """
    Fetches tracks from the provided URL.
    """
    songs_list = []
    offset = 0
    if item_type == 'playlist':
        get_play = dz.get_playlist(item_id)
        items = get_play.tracks
        for item in items:
            track_name = item.title
            track_artist = item.artist.name
            track_album = item.album.title
            cover = item.album.cover_xl
            thumb = item.album.cover_small
            deezer_id = item.id
            songs_list.append({"name": track_name, "artist": track_artist, "album": track_album,"playlist_num": offset + 1,
                                "cover": cover,"deezer_id": deezer_id,"thumb":thumb,"duration":item.duration})
            offset += 1

            if len(items) == offset:
                break
    elif item_type == 'album':
        get_al = dz.get_album(item_id)
        track_album = get_al.title
        cover = get_al.cover_xl
        thumb = get_al.cover_small
        items = get_al.tracks
        for item in items:
            track_name = item.title
            track_artist = item.artist.name
            deezer_id = item.id
            songs_list.append({"name": track_name, "artist": track_artist, "album": track_album,"playlist_num": offset + 1,
                                "cover": cover,"deezer_id": deezer_id,"thumb": thumb,"duration": item.duration})
            offset += 1

            if len(items) == offset:
                break
    elif item_type == 'track':
        get_track = dz.get_track(item_id)
        songs_list.append({"name": get_track.title, "artist": get_track.artist.name, "album": get_track.album.title,"playlist_num": offset + 1,
                            "cover": get_track.album.cover_xl,"deezer_id": get_track.id,"thumb": get_track.album.cover_small,"duration": get_track.duration})

    return songs_list

@sync_to_async
def fetch_spotify_track(client,item_id):
    """
    Fetch tracks from provided item.
    """
    item = client.track(track_id=item_id)
    track_name = item.get("name")
    album_info = item.get("album")
    track_artist = ", ".join([artist['name'] for artist in item['artists']])
    if album_info:
        track_album = album_info.get('name')
        track_year = album_info.get('release_date')[:4] if album_info.get('release_date') else ''
        album_total = album_info.get('total_tracks')
    track_num = item['track_number']
    deezer_id = item_id
    cover = item['album']['images'][0]['url'] if len(item['album']['images']) > 0 else None
    genre = client.artist(artist_id=item['artists'][0]['uri'])['genres'][0] if len(client.artist(artist_id=item['artists'][0]['uri'])['genres']) > 0 else ""
    offset = 0
    return {
            "name": track_name,
            "artist": track_artist,
            "album": track_album,
            "year": track_year,
            "num_tracks": album_total,
            "num": track_num,
            "playlist_num": offset + 1,
            "cover": cover,
            "genre": genre,
            "deezer_id": deezer_id,
        }
@sync_to_async
def download_songs(song, download_directory='.'):
    query = f"{song.get('artist')} - {song.get('name')} Lyrics".replace(":", "").replace("\"", "")
    ydl_opts = {
        'format': "bestaudio",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "nocheckcertificate": True,
        "outtmpl": f"{download_directory}/%(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,

        "nocheckcertificate": True,
        "postprocessors": [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]['id']
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(info)
            path_link = filename
        except Exception as e:
            LOGGER.error(e)
    return path_link

@sync_to_async
def copy(P,A):
    P.copy(LOG_GROUP)
    A.copy(LOG_GROUP)
@sync_to_async
def forward(P,A):
    P.forward(BUG)
    A.forward(BUG)
