import base64

import requests
import os


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

    if token_response.status_code == 200:
        json_data = token_response.json()

        return json_data['access_token']

    return ''


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

    return {'artist': artist_name, 'track': track_name, 'album': album_name}


def get_spotify_music_link(info, token):
    query_value = info['track'] + ' artist: ' + info['artist'] + ' album: ' + info['album']
    params = {'q': query_value, 'type': 'track'}
    headers = {'Authorization': 'Bearer ' + token}
    spotify_search_response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
    json_data = spotify_search_response.json()

    tracks = json_data['tracks']
    items_data = tracks['items'][0]
    external_urls = items_data['external_urls']

    return external_urls['spotify']


def has_spotify_authorization():
    return os.environ.__contains__('SPOTIFY_AUTHORIZATION')


def configure_authorization(client_id, client_secret):
    if client_id != '' and client_secret != '':
        generate_spotify_authorization(client_id, client_secret)
        return True

    return False


def generate_spotify_authorization(client_id, client_secret):
    data = client_id + ':' + client_secret
    base64_bytes = base64.standard_b64encode(data.encode('utf-8'))
    os.environ['SPOTIFY_AUTHORIZATION'] = str(base64_bytes, 'utf-8')


def is_token_valid(token):
    return token != ''
