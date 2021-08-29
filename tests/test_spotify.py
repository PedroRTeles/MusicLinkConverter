import os
from unittest import TestCase
from mockito import kwargs

import requests
from mockito import when

from factory import data_factory

from src import spotify


class SpotifyTest(TestCase):

    def test_when_pass_id_and_secret_should_save_base46(self):
        # Given
        client_id = 'test'
        client_secret = 'test'

        # When
        spotify.generate_spotify_authorization(client_id, client_secret)

        # Then
        self.assertEqual(os.environ['SPOTIFY_AUTHORIZATION'], 'dGVzdDp0ZXN0')

    def test_when_pass_spotify_url_should_return_track_id(self):
        # Given
        spotify_url = 'https://open.spotify.com/track/12345?si=test'

        # When
        track_id = spotify.get_track_id(spotify_url)

        # Then
        self.assertEqual(track_id, '12345')

    def test_when_configure_authorization_correctly_should_return_true(self):
        # Given
        client_id = 'testId'
        client_secret = 'testSecret'

        # When
        configured = spotify.configure_authorization(client_id, client_secret)

        # Then
        self.assertTrue(configured)

    def test_when_configure_authorization_incorrectly_should_return_false(self):
        # Given
        client_id = ''
        client_secret = ''

        # When
        configured = spotify.configure_authorization(client_id, client_secret)

        # Then
        self.assertFalse(configured)

    def test_when_pass_invalid_token_should_return_false(self):
        # Given
        invalid_token = ''

        # When
        is_valid = spotify.is_token_valid(invalid_token)

        # Then
        self.assertFalse(is_valid)

    def test_when_pass_valid_token_should_return_true(self):
        # Given
        valid_token = 'token'

        # When
        is_valid = spotify.is_token_valid(valid_token)

        # Then
        self.assertTrue(is_valid)

    def test_when_spotify_authorization_is_configured_should_return_true(self):
        # Given
        os.environ['SPOTIFY_AUTHORIZATION'] = 'token'

        # When
        is_valid = spotify.has_spotify_authorization()

        # Then
        self.assertTrue(is_valid)

    def test_when_spotify_authorization_is_not_configured_should_return_false(self):
        # Given
        os.environ.clear()

        # When
        is_valid = spotify.has_spotify_authorization()

        # Then
        self.assertFalse(is_valid)

    def test_when_request_successfully_should_return_access_token(self):
        # Given
        os.environ['SPOTIFY_AUTHORIZATION'] = 'test'
        when(requests).post('https://accounts.spotify.com/api/token', **kwargs).thenReturn(
            data_factory.mock_success_spotify_token_response()
        )

        # When
        token = spotify.get_spotify_token()

        # Then
        self.assertEqual(token, 'BQAwALn7Six_RhtNu4LWHnffT7Zsw55uKRxsxtrdjbHRvKFINHhBeI4cGQKBBwwmh88l6T9fQHDbbYiw_zI')

    def test_when_request_fails_should_return_empty_token(self):
        # Given
        os.environ['SPOTIFY_AUTHORIZATION'] = 'test'
        when(requests).post('https://accounts.spotify.com/api/token', **kwargs).thenReturn(
            data_factory.mock_failure_spotify_token_response()
        )

        # When
        token = spotify.get_spotify_token()

        # Then
        self.assertEqual(token, '')

    def test_when_request_search_music_should_return_url(self):
        # Given
        token = 'test'
        track_info = {'track': 'Python Unit Test', 'artist': 'Python', 'album': 'Unit Testing'}
        when(requests).get('https://api.spotify.com/v1/search', **kwargs).thenReturn(
            data_factory.mock_success_spotify_search_music_response()
        )

        # When
        url = spotify.get_spotify_music_link(track_info, token)

        # Then
        self.assertEqual(url, 'https://open.spotify.com/track/UnitTest')

    def test_when_request_track_info_should_return_dictionary(self):
        # Given
        token = 'token'
        track = 'track'
        when(requests).get('https://api.spotify.com/v1/tracks/' + track, **kwargs).thenReturn(
            data_factory.mock_success_spotify_track_detail_response()
        )

        # When
        details = spotify.get_spotify_track_info(token, track)

        # Then
        self.assertEqual(details['artist'], 'Python')
        self.assertEqual(details['album'], 'Unit Testing')
        self.assertEqual(details['track'], 'Python Unit Test')
