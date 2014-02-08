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


def get_inner_archs():
    return os.listdir(localsettings.basedir+"InnerArchs")


def human_readable(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
