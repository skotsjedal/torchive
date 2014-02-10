import localsettings
import os
import re
from operator import itemgetter


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


def get_downloading():
    return os.listdir(localsettings.tmpdir)


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
            extracted = f in get_extracted()
            entries.append((depth, entry[len(localsettings.basedir):], f, human_readable(os.stat(entry).st_size), extracted))
    return entries


def get_all_out():
    entries = []
    for f in get_extracted():
        entries.append((f, human_readable(os.stat(os.path.join(localsettings.outdir, f)).st_size)))
    return sorted(entries, key=itemgetter(0))
