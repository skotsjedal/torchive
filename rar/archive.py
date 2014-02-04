__author__ = 'Skotsj'
import rarfile
from core.core import get_extracted
import localsettings


class Arch:
    name = None
    arch = None
    files = None
    path = None

    def __init__(self, loc):
        self.arch = rarfile.RarFile(loc)
        self.path = loc[len(localsettings.basedir):]
        self.name = loc[loc.rindex("/")+1:]
        print "parsing arch", self.name
        self.files = []
        for f in self.arch.infolist():
            print "append", f.filename
            self.files.append(ContainedFile(f.filename))


class ContainedFile:
    name = None
    extracted = False

    def __init__(self, name):
        print "init", name
        self.name = name
        self.extracted = name in get_extracted()