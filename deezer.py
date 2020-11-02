import requests
import re


def get_deezer_music_link(info):
    query_value = 'artist:"' + info['artist'] + '" track:"' + info['track'] + '" album:"' + info['album'] + '"'
    params = {'q': query_value}
    deezer_track_response = requests.get('https://api.deezer.com/search', params=params)
    json_data = deezer_track_response.json()

    track = json_data['data'][0]

    print('Deezer link: ' + track['link'])


def get_deezer_track_id(deezer_url):
    deezer_response = requests.get(deezer_url)
    track_link = re.search("(?P<url>https?://[^\\s]+/track/[0-9]+)", deezer_response.text).group("url")
    link_info = track_link.split('/')

    return link_info[len(link_info) - 1]


def get_deezer_info(track_id):
    deezer_url = 'https://api.deezer.com/track/' + track_id
    deezer_track_info_response = requests.get(deezer_url)
    json_data = deezer_track_info_response.json()

    album_data = json_data['album']
    artist_data = json_data['artist']

    track_name = json_data['title']
    album_name = album_data['title']
    artist_name = artist_data['name']

    print('Track: ' + track_name)
    print('Artist: ' + artist_name)
    print('Album: ' + album_name)

    return {'track': track_name, 'artist': artist_name, 'album': album_name}
