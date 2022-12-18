import pytest

from .context import Response

@pytest.fixture
def valid_response():
    '''Returns a valid Response object'''
    params = {
        "timestamp": "8/14/2022 0:24:36",
        "url": "https://www.youtube.com/watch?v=Y4LdCdaYppI",
        "start_at": "00:00",
        "end_at": "00:10",
        "platform": "youtube",
        "identifier": "Y4LdCdaYppI",
        "filename": "filename_Y4LdCdaYppI",
        "storage_link": "gs://bucket_uid/filename"
    }
    return Response(params)

@pytest.fixture
def empty_response():
    '''Returns an empty Response object'''
    params = {
        "timestamp": "",
        "url": "",
        "start_at": "",
        "end_at": "",
        "platform": "",
        "identifier": "",
        "filename": "",
        "storage_link": ""
    }
    return Response(params)

@pytest.fixture
def no_timestamp_response():
    '''Returns a Response object without timestamps'''
    params = {
        "timestamp": "8/14/2022 0:24:36",
        "url": "https://www.youtube.com/watch?v=Y4LdCdaYppI",
        "start_at": "",
        "end_at": "",
        "platform": "youtube",
        "identifier": "Y4LdCdaYppI",
        "filename": "filename_Y4LdCdaYppI",
        "storage_link": "gs://bucket_uid/filename"
    }
    return Response(params)

def test_is_valid(valid_response):
    assert valid_response.is_valid()

def test_is_valid_empty(empty_response):
    assert not empty_response.is_valid()

def test_is_valid_no_timestamp(no_timestamp_response):
    assert no_timestamp_response.is_valid()
