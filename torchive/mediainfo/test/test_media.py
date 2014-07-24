from torchive.mediainfo import MediaInfo
from torchive.mediainfo.parser import parse


def test_standard():
    mediainfo = parse("skotsj.live.s01e05.720p.bluray.x264-skotsjprod.mkv")
    assert mediainfo is not None
    assert mediainfo.title == 'skotsj live'
    assert mediainfo.quality == '720p'
    assert mediainfo.source == 'bluray'
    assert mediainfo.codec == 'x264'
    assert mediainfo.grp == 'skotsjprod'


def test_x_sd():
    mediainfo = parse('Oslo.1x4.dvdrip.xvid-naturlig.avi')
    assert mediainfo is not None
    assert mediainfo.title == 'Oslo'
    assert mediainfo.season == 1
    assert mediainfo.ep == 4
    assert mediainfo.grp == 'naturlig'
    assert mediainfo.source == 'dvdrip'
    assert mediainfo.codec == 'xvid'
    assert mediainfo.mtype == MediaInfo.TV


def test_min_tv():
    mediainfo = parse('Oslo.s01e04.avi')
    assert mediainfo is not None
    assert mediainfo.title == 'Oslo'
    assert mediainfo.season == 1
    assert mediainfo.ep == 4
    assert mediainfo.grp is None
    assert mediainfo.mtype == MediaInfo.TV


def test_min_tv_with_epname():
    mediainfo = parse('Oslo.s01e04.Episode.name.avi')
    assert mediainfo is not None
    assert mediainfo.title == 'Oslo'
    assert mediainfo.season == 1
    assert mediainfo.ep == 4
    assert mediainfo.grp is None
    assert mediainfo.info == 'Episode.name'
    assert mediainfo.mtype == MediaInfo.TV


def test_movie():
    mediainfo = parse('Lions.and.Tigers.2013.1080p.BluRay.x264-OpenMovies.mkv')
    assert mediainfo is not None
    assert mediainfo.title == 'Lions and Tigers'
    assert mediainfo.grp == 'OpenMovies'
    assert mediainfo.quality == '1080p'
    assert mediainfo.source == 'BluRay'
    assert mediainfo.codec == 'x264'
    assert mediainfo.year == 2013
    assert mediainfo.mtype == MediaInfo.MOVIE


def test_anime():
    mediainfo = parse('[Fansub] Fakename 14 - The first episode [121BCD42].mkv')
    assert mediainfo is not None
    assert mediainfo.title == 'Fakename'
    assert mediainfo.ep == 14
    assert mediainfo.grp == 'Fansub'
    assert mediainfo.mtype == MediaInfo.ANIME


def test_alt_anime():
    mediainfo = parse('[Fansub] Fakename 14 (720p.HDTV.X264) [121BCD42].mkv')
    assert mediainfo is not None
    assert mediainfo.title == 'Fakename'
    assert mediainfo.ep == 14
    assert mediainfo.grp == 'Fansub'
    assert mediainfo.mtype == MediaInfo.ANIME
