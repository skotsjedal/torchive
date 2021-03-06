from torchive import localsettings

__author__ = 'Skotsj'
from rarfile import RarFile, NeedFirstVolume
from torchive.core.core import get_extracted, get_done, get_inner_archs, human_readable


class Arch:
    name = None
    arch = None
    files = None
    path = None

    def __init__(self, loc):
        self.files = []
        self.path = loc[len(localsettings.BASEDIR):]
        self.name = loc[loc.rindex("/") + 1:]
        try:
            self.arch = RarFile(loc)
            print "archparsed", self.name
        except NeedFirstVolume:
            print "notfirstvolume, skipping", self.name
            return

        for f in self.arch.infolist():
            self.files.append(ContainedFile(f))


class ContainedFile:
    name = None
    extracted = False

    def __init__(self, f):
        print "init", f.filename
        self.name = f.filename
        self.extracted = self.name in get_extracted() or (self.name[-4:] == ".rar" and self.name in get_inner_archs())
        self.seen = self.name in get_done()
        self.size = human_readable(f.file_size)
