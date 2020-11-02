import deezer
import spotify


music_url = input('Enter the music URL: ')

if music_url.__contains__('spotify'):
    print('Converting Spotify link to Deezer link...')
    spotify_token = spotify.get_spotify_token()
    spotify_track_id = spotify.get_track_id(music_url)
    track_info = spotify.get_spotify_track_info(spotify_token, spotify_track_id)

    deezer.get_deezer_music_link(track_info)
elif music_url.__contains__('deezer'):
    print('Converting Deezer link to Spotify link...')
    spotify_token = spotify.get_spotify_token()
    deezer_track_id = deezer.get_deezer_track_id(music_url)
    deezer_track_info = deezer.get_deezer_info(deezer_track_id)

    spotify.get_spotify_music_link(deezer_track_info, spotify_token)

else:
    print('Unknown music platform')
