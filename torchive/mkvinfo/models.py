from abc import ABCMeta, abstractmethod


class Track(object):
    """
        Abstract superclass for other tracktypes
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, track):
        self.name = track.name
        self.track_number = track.number
        self.language = track.language
        self.codec = track.codec_id
        self.default = track.default

    def json(self):
        return self.__dict__


class VideoTrack(Track):
    def __init__(self, track):
        Track.__init__(self, track)
        self.height = track.height
        self.width = track.width


class AudioTrack(Track):
    def __init__(self, track):
        Track.__init__(self, track)
        self.channels = track.channels


class SubTrack(Track):
    def __init__(self, track):
        Track.__init__(self, track)
