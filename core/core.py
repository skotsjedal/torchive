import localsettings
import os


def get_dirs():
    rootentries = [os.path.join(localsettings.basedir, f) for f in os.listdir(localsettings.basedir)]
    dirs = []
    for e in rootentries:
        if os.path.isdir(e):
            dirs.append(e)
    return dirs


def get_extracted():
    return os.listdir(localsettings.outdir)
