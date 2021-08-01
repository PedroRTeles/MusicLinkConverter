import os
from unittest import TestCase

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

        self.assertFalse(is_valid)

    def test_when_pass_valid_token_should_return_true(self):
        # Given
        invalid_token = 'token'

        # When
        is_valid = spotify.is_token_valid(invalid_token)

        self.assertTrue(is_valid)
