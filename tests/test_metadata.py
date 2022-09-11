import pytest

from .context import Metadata

@pytest.fixture
def valid_metadata():
    '''Returns a valid metadata object'''
    return Metadata(platform="youtube", identifier="dQw4w9WgXcQ", filename="watch_me_Youtube[dQw4w9WgXcQ]")

@pytest.fixture
def invalid_metadata():
    '''Returns an invalid metadata object'''
    return Metadata(platform="crunchyroll", identifier="342342", filename="weebcity[342342]")

def test_is_valid(valid_metadata):
    assert valid_metadata.is_valid()

def test_is_invalid(invalid_metadata):
    assert not invalid_metadata.is_valid()

def test_platform_parsed(valid_metadata):
    assert valid_metadata.platform == "youtube"

def test_identifier_parsed(valid_metadata):
    assert valid_metadata.identifier == "dQw4w9WgXcQ"

def test_key(valid_metadata):
    assert valid_metadata.key() == "youtube-dQw4w9WgXcQ"
