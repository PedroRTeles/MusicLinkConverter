import os
from unittest import TestCase
from unittest.mock import patch
from mockito import kwargs

import requests
from mockito import when

from factory import data_factory

import spotify


class SpotifyTest(TestCase):

    def test_when_pass_id_and_secret_should_save_base46(self):
        # Given
        client_id = 'test'
        client_secret = 'test'

        # When
        spotify.generate_spotify_authorization(client_id, client_secret)

        # Then
        self.assertEquals(os.environ['SPOTIFY_AUTHORIZATION'], 'dGVzdDp0ZXN0')

    def test_when_pass_spotify_url_should_return_track_id(self):
        # Given
        spotify_url = 'https://open.spotify.com/track/12345?si=test'

        # When
        track_id = spotify.get_track_id(spotify_url)

        # Then
        self.assertEquals(track_id, '12345')

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
        invalid_token = 'token'

        # When
        is_valid = spotify.is_token_valid(invalid_token)

        # Then
        self.assertTrue(is_valid)

    def test_when_request_successfully_should_return_access_token(self):
        # Given
        os.environ['SPOTIFY_AUTHORIZATION'] = 'test'
        when(requests).post('https://accounts.spotify.com/api/token', **kwargs).thenReturn(
            data_factory.mock_success_spotify_token_response()
        )

        # When
        token = spotify.get_spotify_token()

        # Then
        self.assertEquals(token, 'BQAwALn7Six_RhtNu4LWHnffT7Zsw55uKRxsxtrdjbHRvKFINHhBeI4cGQKBBwwmh88l6T9fQHDbbYiw_zI')

    def test_when_request_fails_should_return_empty_token(self):
        # Given
        os.environ['SPOTIFY_AUTHORIZATION'] = 'test'
        when(requests).post('https://accounts.spotify.com/api/token', **kwargs).thenReturn(
            data_factory.mock_failure_spotify_token_response()
        )

        # When
        token = spotify.get_spotify_token()

        # Then
        self.assertEquals(token, '')
