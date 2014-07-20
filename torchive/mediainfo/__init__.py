__author__ = 'Skotsj'

PATH = ""
if '__file__' in globals():
    import os

    PATH = str(os.path.dirname(__file__))
    if PATH:
        PATH += "/"


class MediaInfo:
    def __init__(self):
        self.mtype = None
        self.grp = None
        self.title = None
        self.season = None
        self.ep = None
        self.info = None
        self.quality = None
        self.source = None
        self.year = None
        self.ft = None

    def __str__(self):
        return str(self.__dict__)


class ImdbInfo:
    def __init__(self):
        self.title = None
        self.imdbid = None
        self.seasons = {}
        self.image = None
        self.year = None
        self.rating = None

    def get_epcount(self, season):
        return self.seasons[season]

    def get_seasoncount(self):
        return len(self.seasons)
