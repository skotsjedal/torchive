__author__ = 'Skotsj'
import rarfile
from core.core import get_extracted, get_inner_archs, human_readable
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
        print "archparse", self.name
        self.files = []
        for f in self.arch.infolist():
            self.files.append(ContainedFile(f))


class ContainedFile:
    name = None
    extracted = False

    def __init__(self, f):
        print "init", f.filename
        self.name = f.filename
        self.extracted = self.name in get_extracted() or (self.name[-4:] == ".rar" and self.name in get_inner_archs())
        self.size = human_readable(f.file_size)
