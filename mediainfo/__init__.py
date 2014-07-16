__author__ = 'Skotsj'


class MediaInfo:
    def __init__(self):
        self.mtype = None
        self.filename = None
        self.grp = None
        self.title = None
        self.season = None
        self.ep = None
        self.quality = None
        self.source = None
        self.year = None
        self.ft = None

    def __str__(self):
        return str(self.__dict__)
