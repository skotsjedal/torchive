__author__ = 'Skotsj'
import rarfile


class Arch:
    name = None
    arch = None
    files = None

    def __init__(self, loc):
        self.arch = rarfile.RarFile(loc)
        loc = loc[loc.rindex("/")+1:]
        self.name = loc
        print "parsing arch", loc
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