from torchive.mediainfo.mediainfo import search_imdb

__author__ = 'Skotsj'


def test_search():
    result = search_imdb('downton abbey')
    assert result is not None
    print result
    assert result.imdbid == "tt1606375"
    assert result.title is not None
    assert len(result.seasons) == 0
    assert result.year is not None
    assert result.image is not None
    assert result.rating is not None


def test_episodes():
    result = search_imdb('downton abbey', with_episodes=True)
    assert result is not None
    print result
    assert result.imdbid == "tt1606375"
    assert result.get_seasoncount() >= 5
    assert result.get_epcount(1) == 7
    assert result.get_epcount(2) == 9


def test_episodes_for_movie():
    result = search_imdb('x-men', with_episodes=True)
    assert result is not None
    print result
    assert result.imdbid == "tt0120903"
    assert result.get_seasoncount() == 0
