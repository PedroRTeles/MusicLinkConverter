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

            print('Track: ' + track_info['track'])
            print('Artist: ' + track_info['artist'])
            print('Album: ' + track_info['album'])

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

            link = spotify.get_spotify_music_link(deezer_track_info, spotify_token)

            print('Spotify link: ', link)
        else:
            print('Could not generate Spotify Token.')
            print('Please try again.')
    else:
        print('Unknown music platform')


if spotify.has_spotify_authorization():
    convert_music()
else:
    print('You need to inform a Spotify authorization key.')
    print('To create one access: https://developer.spotify.com/dashboard/')
    print('and follow the steps to create an app.')
    print('')

    client_id = input('Enter the Client ID: ')
    client_secret = input('Enter the Client Secret: ')

    if spotify.configure_authorization(client_id, client_secret):
        convert_music()
    else:
        print('Sorry, in order to use this app you need a Spotify authorization key.')
