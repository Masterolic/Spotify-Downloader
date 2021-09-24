#Main Script https://github.com/SathyaBhat/spotify-dl

import sys
from os import path
from spotify_dl.utils import sanitize
import youtube_dl
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
import urllib.request


def fetch_tracks(sp, item_type, url):
    """
    Fetches tracks from the provided URL.
    :param sp: Spotify client
    :param item_type: Type of item being requested for: album/playlist/track
    :param url: URL of the item
    :return Dictionary of song and artist
    """
    songs_list = []
    offset = 0

    if item_type == 'playlist':
        while True:
            items = sp.playlist_items(playlist_id=url,

                                      fields='items.track.name,items.track.artists(name, uri),'
                                             'items.track.album(name, release_date, total_tracks, images),'

                                             'items.track.track_number,total, next,offset,'
                                             'items.track.id',
                                      additional_types=['track'], offset=offset)
            total_songs = items.get('total')
            for item in items['items']:
                track_info = item.get('track')
                track_album_info = track_info.get('album')

                track_num = track_info.get('track_number')
                spotify_id = track_info.get('id')
                track_name = track_info.get('name')
                track_artist = ", ".join([artist['name'] for artist in track_info.get('artists')])

                if track_album_info:
                    track_album = track_album_info.get('name')
                    track_year = track_album_info.get('release_date')[:4] if track_album_info.get('release_date') else ''
                    album_total = track_album_info.get('total_tracks')

                if len(item['track']['album']['images']) > 0:
                    cover = item['track']['album']['images'][0]['url']
                else:
                    cover = None

                if len(sp.artist(artist_id=item['track']['artists'][0]['uri'])['genres']) > 0:
                    genre = sp.artist(artist_id=item['track']['artists'][0]['uri'])['genres'][0]
                else:
                    genre = ""
                songs_list.append({"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
                                   "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
                                   "cover": cover, "genre": genre, "spotify_id": spotify_id})
                offset += 1

            if total_songs == offset:
                break

    elif item_type == 'album':
        while True:
            album_info = sp.album(album_id=url)
            items = sp.album_tracks(album_id=url)
            total_songs = items.get('total')
            track_album = album_info.get('name')
            track_year = album_info.get('release_date')[:4] if album_info.get('release_date') else ''
            album_total = album_info.get('total_tracks')
            if len(album_info['images']) > 0:
                cover = album_info['images'][0]['url']
            else:
                cover = None
            if len(sp.artist(artist_id=album_info['artists'][0]['uri'])['genres']) > 0:
                genre = sp.artist(artist_id=album_info['artists'][0]['uri'])['genres'][0]
            else:
                genre = ""
            for item in items['items']:
                track_name = item.get('name')
                track_artist = ", ".join([artist['name'] for artist in item['artists']])
                track_num = item['track_number']
                spotify_id = item.get('id')
                songs_list.append({"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
                                   "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
                                   "cover": cover, "genre": genre, "spotify_id": spotify_id})
                offset += 1

            if total_songs == offset:
                break

    elif item_type == 'track':
        items = sp.track(track_id=url)
        track_name = items.get('name')
        album_info = items.get('album')
        track_artist = ", ".join([artist['name'] for artist in items['artists']])
        if album_info:
            track_album = album_info.get('name')
            track_year = album_info.get('release_date')[:4] if album_info.get('release_date') else ''
            album_total = album_info.get('total_tracks')
        track_num = items['track_number']
        spotify_id = items['id']
        if len(items['album']['images']) > 0:
            cover = items['album']['images'][0]['url']
        else:
            cover = None
        if len(sp.artist(artist_id=items['artists'][0]['uri'])['genres']) > 0:
            genre = sp.artist(artist_id=items['artists'][0]['uri'])['genres'][0]
        else:
            genre = ""
        songs_list.append({"name": track_name, "artist": track_artist, "album": track_album, "year": track_year,
                           "num_tracks": album_total, "num": track_num, "playlist_num": offset + 1,
                           "cover": cover, "genre": genre, "spotify_id": spotify_id})

    return songs_list


def parse_spotify_url(url):
    """
    Parse the provided Spotify playlist URL and determine if it is a playlist, track or album.
    :param url: URL to be parsed

    :return tuple indicating the type and id of the item
    """
    if url.startswith("spotify:"):
        print("gib meh spotify limk.")
    parsed_url = url.replace("https://open.spotify.com/", "")
    item_type = parsed_url.split("/")[0]
    return item_type


def get_item_name(sp, item_type, item_id):
    """
    Fetch the name of the item.
    :param sp: Spotify Client
    :param item_type: Type of the item
    :param item_id: id of the item
    :return String indicating the name of the item
    """
    if item_type == 'playlist':
        name = sp.playlist(playlist_id=item_id, fields='name').get('name')
    elif item_type == 'album':
        name = sp.album(album_id=item_id).get('name')
    elif item_type == 'track':
        name = sp.track(track_id=item_id).get('name')
    return sanitize(name)


def validate_spotify_url(url):
    """
    Validate the URL and determine if the item type is supported.
    :return Boolean indicating whether or not item is supported
    """
    item_type, item_id = parse_spotify_url(url)
    if item_type not in ['album', 'track', 'playlist']:
        print("Only albums/tracks/playlists are supported")
        return False
    if item_id is None:
        print("Couldn't get a valid id")
        return False
    return True

def default_filename(song):
    return sanitize(f"{song[0]['artist']} - {song[0]['name']}", '#')
def default_filenames(song):
    return sanitize(f"{song['artist']} - {song['name']}", '#')

def download_song(song, download_directory, format_string='bestaudio/best', skip_mp3=False,
                   keep_playlist_order=False, file_name_f=default_filename):
    """
    Downloads songs from the YouTube URL passed to either current directory or download_directory, is it is passed.
    :param songs: Dictionary of songs and associated artist
    :param download_directory: Location where to save
    :param format_string: format string for the file conversion
    :param skip_mp3: Whether to skip conversion to MP3
    :param keep_playlist_order: Whether to keep original playlist ordering. Also, prefixes songs files with playlist num
    :param file_name_f: optional func(song) -> str that returns a filename for the download (without extension)
    """
    print(f"Downloading to {download_directory}")
    query = f"{song[0]['artist']} - {song[0]['name']} Lyrics".replace(":", "").replace("\"", "")
    download_archive = path.join(download_directory, 'downloaded_songs.txt')
    file_name = file_name_f(song)
    file_path = path.join(download_directory, file_name)

    outtmpl = f"{file_path}.%(ext)s"
    ydl_opts = {
        'format': format_string,
        'download_archive': download_archive,
        'outtmpl': outtmpl,
        'default_search': 'ytsearch',
        'noplaylist': True,
        'postprocessor_args': ['-metadata', 'title=' + song[0]['name'],
                               '-metadata', 'artist=' + song[0]['artist'],
                               '-metadata', 'album=' + song[0]['album']]
    }
    if not skip_mp3:
        mp3_postprocess_opts = {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }
        ydl_opts['postprocessors'] = [mp3_postprocess_opts.copy()]

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([query])
        except Exception as e:
            print(e)
            print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))

    if not skip_mp3:
        try:
            song_file = MP3(path.join(f"{file_path}.mp3"), ID3=EasyID3)
        except mutagen.MutagenError as e:
            print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))
        song_file['date'] = song[0]['year']
        if keep_playlist_order:
            song_file['tracknumber'] = str(song[0]['playlist_num'])
        else:
            song_file['tracknumber'] = str(song[0]['num']) + '/' + str(song[0]['num_tracks'])
        song_file['genre'] = song[0]['genre']
        song_file.save()
        song_file = MP3(f"{file_path}.mp3", ID3=ID3)
        if song[0]['cover'] is not None:
            song_file.tags['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=urllib.request.urlopen(song[0]['cover']).read()
            )
        song_file.save()
        print (f"{file_path}.mp3")
        return (f"{file_path}.mp3")

def download_songs(song, download_directory, format_string='bestaudio/best', skip_mp3=False,
                   keep_playlist_order=False, file_name_f=default_filenames):
    """
    Downloads songs from the YouTube URL passed to either current directory or download_directory, is it is passed.
    :param songs: Dictionary of songs and associated artist
    :param download_directory: Location where to save
    :param format_string: format string for the file conversion
    :param skip_mp3: Whether to skip conversion to MP3
    :param keep_playlist_order: Whether to keep original playlist ordering. Also, prefixes songs files with playlist num
    :param file_name_f: optional func(song) -> str that returns a filename for the download (without extension)
    """
    print(f"Downloading to {download_directory}")
    query = f"{song['artist']} - {song['name']} Lyrics".replace(":", "").replace("\"", "")
    print(query)
    download_archive = path.join(download_directory, 'downloaded_songs.txt')
    file_name = file_name_f(song)
    file_path = path.join(download_directory, file_name)

    outtmpl = f"{file_path}.%(ext)s"
    ydl_opts = {
        'format': format_string,
        'download_archive': download_archive,
        'outtmpl': outtmpl,
        'default_search': 'ytsearch',
        'noplaylist': True,
        'postprocessor_args': ['-metadata', 'title=' + song['name'],
                               '-metadata', 'artist=' + song['artist'],
                               '-metadata', 'album=' + song['album']]
    }
    if not skip_mp3:
        mp3_postprocess_opts = {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }
        ydl_opts['postprocessors'] = [mp3_postprocess_opts.copy()]

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([query])
        except Exception as e:
            print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))

    if not skip_mp3:
        try:
            song_file = MP3(path.join(f"{file_path}.mp3"), ID3=EasyID3)
        except mutagen.MutagenError as e:
            print('Failed to download: {}, please ensure YouTubeDL is up-to-date. '.format(query))
        song_file['date'] = song['year']
        if keep_playlist_order:
            song_file['tracknumber'] = str(song['playlist_num'])
        else:
            song_file['tracknumber'] = str(song['num']) + '/' + str(song['num_tracks'])
        song_file['genre'] = song['genre']
        song_file.save()
        song_file = MP3(f"{file_path}.mp3", ID3=ID3)
        if song['cover'] is not None:
            song_file.tags['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3, desc=u'Cover',
                data=urllib.request.urlopen(song['cover']).read()
            )
        song_file.save()
        print (f"{file_path}.mp3")
        return (f"{file_path}.mp3")
