import pytest

from .context import Video

@pytest.fixture
def valid_video():
    '''Returns a valid video object'''
    return Video.create("watch_me_Youtube[dQw4w9WgXcQ]")

@pytest.fixture
def tiktok_video_with_youtube():
    '''Returns a tiktok video with youtube in the title'''
    return Video.create("youtube_video_tiktok[18382921]")

@pytest.fixture
def youtube_video_with_tiktok():
    '''Returns a youtube video with tiktok in the title'''
    return Video.create("tiktok_video_yOuTube[abc123]")

def test_is_valid(valid_video):
    assert valid_video.platform == "youtube"
    assert valid_video.identifier == "dQw4w9WgXcQ"

def test_tiktok_video_with_youtube(tiktok_video_with_youtube):
    assert tiktok_video_with_youtube.platform == "tiktok"
    assert tiktok_video_with_youtube.identifier == "18382921"

def test_youtube_video_with_tiktok(youtube_video_with_tiktok):
    assert youtube_video_with_tiktok.platform == "youtube"
    assert youtube_video_with_tiktok.identifier == "abc123"
