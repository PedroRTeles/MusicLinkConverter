import argparse
import sys
import spotify
import deezer


def convert_to_deezer():
    print('Converting Spotify link to Deezer link...')

    spotify_token = spotify.get_spotify_token()

    if spotify.is_token_valid(spotify_token):
        spotify_track_id = spotify.get_track_id(url)
        track_info = spotify.get_spotify_track_info(spotify_token, spotify_track_id)

        deezer.get_deezer_music_link(track_info)
    else:
        spotify.token_error_message()


def convert_to_spotify():
    print('Converting Deezer link to Spotify link...')

    spotify_token = spotify.get_spotify_token()

    if spotify.is_token_valid(spotify_token):
        deezer_track_id = deezer.get_deezer_track_id(url)
        deezer_track_info = deezer.get_deezer_info(deezer_track_id)

        spotify.get_spotify_music_link(deezer_track_info, spotify_token)
    else:
        spotify.token_error_message()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', help="Music url", type=str, required=True)
    parser.add_argument('--id', '-i', help="Spotify client id", type=str)
    parser.add_argument('--secret', '-s', help="Spotify client secret", type=str)

    url = parser.parse_args().__getattribute__('url')
    client_id = parser.parse_args().__getattribute__('id')
    client_secret = parser.parse_args().__getattribute__('secret')

    if not spotify.has_spotify_authorization():
        if client_id is None or client_secret is None:
            print('Spotify authorization token not configured')
            print('Input client id and secret via -i and -s arguments')
            sys.exit()
        else:
            spotify.generate_spotify_authorization(client_id, client_secret)

    if url.__contains__('spotify'):
        convert_to_deezer()
    elif url.__contains__('deezer'):
        convert_to_spotify()
    else:
        print('Unknown music platform')
