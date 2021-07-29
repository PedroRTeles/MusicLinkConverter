import deezer
import spotify


def convert_music():
    music_url = input('Enter the music URL: ')
    if music_url.__contains__('spotify'):
        print('Converting Spotify link to Deezer link...')
        spotify_token = spotify.get_spotify_token()

        if spotify.is_token_valid(spotify_token):
            spotify_track_id = spotify.get_track_id(music_url)
            track_info = spotify.get_spotify_track_info(spotify_token, spotify_track_id)

            deezer.get_deezer_music_link(track_info)
        else:
            print('Could not generate Spotify Token.')
            print('Please try again.')
    elif music_url.__contains__('deezer'):
        print('Converting Deezer link to Spotify link...')
        spotify_token = spotify.get_spotify_token()

        if spotify.is_token_valid(spotify_token):
            deezer_track_id = deezer.get_deezer_track_id(music_url)
            deezer_track_info = deezer.get_deezer_info(deezer_track_id)

            spotify.get_spotify_music_link(deezer_track_info, spotify_token)
        else:
            print('Could not generate Spotify Token.')
            print('Please try again.')
    else:
        print('Unknown music platform')


if spotify.has_spotify_authorization():
    convert_music()
else:
    if spotify.configure_authorization():
        convert_music()
    else:
        print('Sorry, in order to use this app you need a Spotify authorization key.')
