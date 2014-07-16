from mediainfo.parser import parse


def test_standard():
    mediainfo = parse("skotsj.live.s01e05.720p.bluray.x264-skotsjprod.mkv")
    assert mediainfo is not None
    assert mediainfo.title == 'skotsj live'
    mediainfo = parse('derp.S09E12.720p.HDTV.X264-SillyTV.mkv')
    assert mediainfo.title == 'derp'
    assert mediainfo is not None


def test_x_sd():
    mediainfo = parse('Oslo.1x4.dvdrip.xvid-naturlig.avi')
    assert mediainfo.title == 'Oslo'
    assert mediainfo.season == 1
    assert mediainfo.ep == 4
    assert mediainfo.grp == 'naturlig'
    assert mediainfo is not None
