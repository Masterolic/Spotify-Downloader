import requests,deezer


client = deezer.Client()

def sanitize(name, replace_with=''):
    """
    Removes some of the reserved characters from the name so it can be saved
    :param name: Name to be cleaned up
    :return string containing the cleaned name
    """
    clean_up_list = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|", "\0", "$"]
    for x in clean_up_list:
        name = name.replace(x, replace_with)
    return name

def parse_deezer_url(url):
    """
    Parse the provided deezer playlist URL and determine if it is a playlist, track or album.
    :param url: URL to be parsed
    :return tuple indicating the type and id of the item
    """
    url = requests.get(url).url
    parsed_url = url.replace("https://www.deezer.com/", "")
    item_type = parsed_url.split("/")[1]
    item_id = parsed_url.split("/")[2].split("?")[0]
    return item_type, item_id

def fetch_tracks(sp, item_type, url):
    """
    Fetches tracks from the provided URL.
    :param item_type: Type of item being requested for: album/playlist/track
    """
    songs_list = []
    offset = 0
    if item_type == 'track':


print(parse_deezer_url("https://deezer.page.link/B4W19UroyPP8wRVm6"))
