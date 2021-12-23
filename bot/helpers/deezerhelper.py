import requests,deezer
import yt_dlp as youtube_dl
import urllib.request
from os import path
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
import mutagen
from mutagen.easyid3 import EasyID3


client = deezer.Client()

def sanitize(name, replace_with=''):
    clean_up_list = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\0", "$","\""]
    for x in clean_up_list:
        name = name.replace(x, replace_with)
    return name

def parse_deezer_url(url):
    url = requests.get(url).url
    parsed_url = url.replace("https://www.deezer.com/", "")
    item_type = parsed_url.split("/")[1]
    item_id = parsed_url.split("/")[2].split("?")[0]
    return item_type, item_id

def get_item_name(dz, item_type, item_id):
    if item_type == 'playlist':
        name = dz.get_playlist(item_id).title
    elif item_type == 'album':
        name = dz.get_album(item_id).title
    elif item_type == 'track':
        name = dz.get_track(item_id).title
    return sanitize(name)


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
            #print(item)
            cover = item.album.cover_xl
            deezer_id = item.id
            songs_list.append({"name": track_name, "artist": track_artist, "album": track_album,"playlist_num": offset + 1,
                                "cover": cover,"deezer_id": deezer_id})
            offset += 1

            if len(items) == offset:
                break

    elif item_type == 'album':
        get_al = client.get_album(item_id)
        track_album = get_al.title
        cover = get_al.cover_xl
        items = get_al.tracks
        for item in items:
            track_name = item.title
            track_artist = item.artist.name
            deezer_id = item.id
            songs_list.append({"name": track_name, "artist": track_artist, "album": track_album,"playlist_num": offset + 1,
                                "cover": cover,"deezer_id": deezer_id})
            offset += 1

            if len(items) == offset:
                break
    elif item_type == 'track':
        get_track = client.get_track(item_id)
        songs_list.append({"name": get_track.title, "artist": get_track.artist.name, "album": get_track.album.title,"playlist_num": offset + 1,
                            "cover": get_track.album.cover_xl,"deezer_id": get_track.id})

    return songs_list

def default_filename(song):
    return sanitize(f"{song.get('name')} - {song.get('album')} - {song.get('artist')}", '#')

def download_songs(songs, download_directory='.', format_string="bestaudio/best", skip_mp3=False,
                   keep_playlist_order=False, file_name_f=default_filename):
    path_links = []

    for song in songs:
        query = f"{song.get('artist')} - {song.get('name')} Lyrics".replace(":", "").replace("\"", "")
        file_name = file_name_f(song)
        file_path = path.join(download_directory,f"{song.get('album')}", file_name)
        path_links.append(f"{file_path}.mp3")

        outtmpl = f"{file_path}.%(ext)s"
        ydl_opts = {
            'format': format_string,
            'default_search': 'ytsearch',
            "preferredcodec": "mp3",
            'noplaylist': True,
            "outtmpl": f"{file_path}.mp3",
            'postprocessor_args': [
                '-metadata',
                'title=' + song.get('name'),
                '-metadata',
                'artist=' + song.get('artist'),
                '-metadata',
                'album=' + song.get('album'),
            ],
        }

        if not skip_mp3:
            mp3_postprocess_opts = {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }
            ydl_opts['postprocessors'] = [mp3_postprocess_opts.copy()]

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([query])
            except Exception as e:
                print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))
                continue
        if not skip_mp3:
            try:
                song_file = MP3(path.join(f"{file_path}.mp3"), ID3=EasyID3)
            except mutagen.MutagenError as e:
                print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))
                continue
            song_file = MP3(f"{file_path}.mp3", ID3=ID3)
            if song.get('cover') is not None:
                song_file.tags['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3, desc=u'Cover',
                    data=urllib.request.urlopen(song.get('cover')).read()
                )
            song_file.save()
    return path_links

#11474676
def artist_data(dz,artist_id):
    artist = dz.get_artist(artist_id)
    name = artist.name
    link = artist.link
    picture = artist.picture_xl
    number_of_album = artist.nb_album
    albums = artist.get_albums()
    return name,link,picture,number_of_album,albums


def download_now(dz,url,download_directory="."):
    parsed = parse_deezer_url(url)
    fetched = fetch_tracks(dz,parsed[0],parsed[1])
    return download_songs(fetched,download_directory=download_directory)
