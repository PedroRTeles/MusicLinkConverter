import requests
import os
import re


def get_track_id(spotify_url):
    url_keyword = "/track/"
    slice_start = spotify_url.find(url_keyword) + len(url_keyword)

    track_id = spotify_url[slice_start:]

    if track_id.__contains__("?"):
        slice_end = track_id.find("?")
        track_id = track_id[:slice_end]

    return track_id


def get_spotify_token():
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic ' + os.environ['SPOTIFY_AUTHORIZATION']}
    data = {'grant_type': 'client_credentials'}
    token_response = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
    json_data = token_response.json()

    return json_data['access_token']


def get_spotify_track_info(token, track):
    url = 'https://api.spotify.com/v1/tracks/' + track
    headers = {'Authorization': 'Bearer ' + token}
    track_response = requests.get(url, headers=headers)
    json_data = track_response.json()

    artists = json_data['artists']
    album = json_data['album']
    artist_name = artists[0]['name']
    track_name = json_data['name']
    album_name = album['name']

    print('Track: ' + track_name)
    print('Artist: ' + artist_name)
    print('Album: ' + album_name)

    return {'artist': artist_name, 'track': track_name, 'album': album_name}


def get_deezer_music_link(info):
    query_value = 'artist:"' + info['artist'] + '" track:"' + info['track'] + '" album:"' + info['album'] + '"'
    params = {'q':  query_value}
    deezer_track_response = requests.get('https://api.deezer.com/search', params=params)
    json_data = deezer_track_response.json()

    track = json_data['data'][0]

    print('Deezer link: ' + track['link'])


def get_deezer_track_id(deezer_url):
    deezer_response = requests.get(deezer_url)
    track_link = re.search("(?P<url>https?://[^\s]+/track/[0-9]+)", deezer_response.text).group("url")
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


def get_spotify_music_link(info, token):
    query_value = info['track'] + ' artist: ' + info['artist'] + ' album: ' + info['album']
    params = {'q': query_value, 'type': 'track'}
    headers = {'Authorization': 'Bearer ' + token}
    spotify_search_response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
    json_data = spotify_search_response.json()

    tracks = json_data['tracks']
    items_data = tracks['items'][0]
    external_urls = items_data['external_urls']

    print('Spotify link: ' + external_urls['spotify'])


music_url = input('Enter the music URL: ')

if music_url.__contains__('spotify'):
    print('Converting Spotify link to Deezer link...')
    spotify_token = get_spotify_token()
    spotify_track_id = get_track_id(music_url)
    track_info = get_spotify_track_info(spotify_token, spotify_track_id)

    get_deezer_music_link(track_info)
elif music_url.__contains__('deezer'):
    print('Converting Deezer link to Spotify link...')
    spotify_token = get_spotify_token()
    deezer_track_id = get_deezer_track_id(music_url)
    deezer_track_info = get_deezer_info(deezer_track_id)

    get_spotify_music_link(deezer_track_info, spotify_token)

else:
    print('Unknown music platform')
