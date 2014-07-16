from mediainfo import MediaInfo

__author__ = 'Skotsj'


def tv(Title=None, Episode=None, Quality=None, Source=None, Codec=None, Group=None, Filetype=None):
    m = MediaInfo()
    m.mtype = u'TV'
    m.title = Title[1]
    m.season, m.ep = int(Episode[0]), int(Episode[1])
    m.quality = Quality[0] if Quality is not None else None
    m.source = Source[0]
    m.codec = (Codec[0], Codec[1])
    m.grp = Group[0]
    m.ft = Filetype[0]
    return m


def movie(Title=None, Year=None, Quality=None, Source=None, Codec=None, Group=None, Filetype=None):
    m = MediaInfo()
    m.mtype = u'Movie'
    m.title = Title[1]
    m.year = Year[0]
    m.quality = Quality[0] if Quality is not None else None
    m.source = Source[0]
    m.codec = (Codec[0], Codec[1])
    m.grp = Group[0]
    m.ft = Filetype[0]
    return m


def anime(Group=None, Title=None, Episode=None, Filetype=None):
    m = MediaInfo()
    m.mtype = u'Anime'
    m.title = Title[1]
    m.ep = Episode[1]
    m.grp = Group[0]
    m.ft = Filetype[0]
    return m

functions = {
    'TV': tv,
    'Movie': movie,
    'Anime': anime
}

