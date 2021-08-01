import os


def get_json_mock(file):
    path = os.path.dirname(__file__) + '/../../mocks/' + file
    return bytes(open(path).read(), 'utf-8')
