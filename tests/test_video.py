import pytest

from .context import Video

@pytest.fixture
def valid_video():
    '''Returns a valid video object'''
    return Video.create({ "platform": "youtube", "identifier": "dQw4w9WgXcQ" })

def test_is_valid(valid_video):
    assert valid_video.is_valid()

def test_platform_parsed(valid_video):
    assert valid_video.platform == "youtube"

def test_identifier_parsed(valid_video):
    assert valid_video.identifier == "dQw4w9WgXcQ"

def test_key(valid_video):
    assert valid_video.key() == "youtube-dQw4w9WgXcQ"
