from requests import Response
from .helper import json_helper


def mock_success_spotify_token_response():
    response = Response()
    response.status_code = 200
    response._content = json_helper.get_json_mock('spotify_token_response_success.json')

    return response


def mock_failure_spotify_token_response():
    response = Response()
    response.status_code = 500
    response._content = None

    return response


def mock_success_spotify_search_music_response():
    response = Response()
    response.status_code = 200
    response._content = json_helper.get_json_mock('spotify_search_response_success.json')

    return response


def mock_success_spotify_track_detail_response():
    response = Response()
    response.status_code = 200
    response._content = json_helper.get_json_mock('spotify_track_detail_response_success.json')

    return response
