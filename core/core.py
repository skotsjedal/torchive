import localsettings
import os
import re

RARTEMP = 'InnerArchs'
RARFILE = re.compile('.*\.r(\d\d|ar)')

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
    return os.listdir(localsettings.basedir+RARTEMP)


def human_readable(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def get_all(depth=0, folder=localsettings.basedir):
    entries = []
    for f in os.listdir(folder):
        if f == RARTEMP or RARFILE.match(f):
            continue
        entry = os.path.join(folder, f)
        
        if os.path.isdir(entry):
            entries += get_all(depth+1, entry)
        else:
            entries.append((depth, entry, f, human_readable(os.stat(entry).st_size)))
    return entries
