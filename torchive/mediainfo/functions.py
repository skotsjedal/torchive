from torchive.mediainfo import MediaInfo

__author__ = 'Skotsj'


def tv(Title=None, Episode=None, Info=None, Source=None, Codec=None, Group=None, Filetype=None):
    m = MediaInfo()
    m.mtype = MediaInfo.TV
    m.title = Title[1]
    m.season, m.ep = int(Episode[0]), int(Episode[1])
    if Info is not None:
        m.info = Info[0][0] if Info[0] is not None else None
        m.quality = Info[1][0] if Info[1] is not None else None
    m.source = Source[0]
    m.codec = Codec[0]
    m.grp = Group[0]
    m.ft = Filetype[0]
    return m


def movie(Title=None, Year=None, Quality=None, Source=None, Codec=None, Group=None, Filetype=None):
    m = MediaInfo()
    m.mtype = MediaInfo.MOVIE
    m.title = Title[1]
    m.year = Year[0]
    m.quality = Quality[0] if Quality is not None else None
    m.source = Source[0]
    m.codec = Codec[0]
    m.grp = Group[0] if Group is not None else None
    m.ft = Filetype[0]
    return m


def anime(Group=None, Title=None, Episode=None, Text=None, Filetype=None):
    m = MediaInfo()
    m.mtype = MediaInfo.ANIME
    m.title = Title[1]
    m.ep = Episode[1]
    m.info = Text[0] if Text is not None else None
    m.grp = Group[0]
    m.ft = Filetype[0]
    return m

functions = {
    'TV': tv,
    'Movie': movie,
    'Anime': anime
}

