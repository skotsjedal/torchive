import localsettings
import os
import re
import datetime
import hashlib

RARTEMP = u'InnerArchs'
RARFILE = re.compile('.*\.r(\d\d|ar)')


def hashfolder(string):
    digests = []
    folders = string.split('/')
    partial = ''
    for f in folders:
        partial += '/'+f.encode('utf-8')
        h = hashlib.sha1(partial)
        hexd = h.hexdigest()[0:12]
        digests.append(hexd)
    fullhex = ' '.join(digests)
    print string, fullhex
    return fullhex


def get_file_hash(name):
    fsize = os.stat(localsettings.outdir + name).st_size
    hashbase = name + str(fsize) + localsettings.hashsalt
    return hashlib.sha1(hashbase).hexdigest()[0:12]


def get_dirs():
    rootentries = [os.path.join(localsettings.basedir, f) for f in os.listdir(localsettings.basedir)]
    dirs = []
    for e in rootentries:
        if os.path.isdir(e):
            dirs.append(e)
    return dirs


def get_done():
    return os.listdir(localsettings.donedir)

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
    if isinstance(folder, str):
        folder = unicode(folder, 'UTF-8')
    for f in os.listdir(folder):
        foldername = folder[folder.rindex('/')+1:]
        if not RARTEMP == foldername and RARFILE.match(f):
            continue
        entry = os.path.join(folder, f)
        itemname = entry[len(localsettings.basedir):]
        idx = hashfolder(itemname)
        if os.path.isdir(entry):
            if not f == RARTEMP:
                entries.append((depth, itemname, f, "Directory", False, False, idx))
            entries += get_all(depth+1, entry)
        else:
            extracted = f in get_extracted()
            entries.append((depth, itemname, f, human_readable(os.stat(entry).st_size), extracted, f in get_done(), idx))
    entries = sorted(entries, key=lambda i: i[1].lower())
    return entries


def get_all_out():
    entries = []
    for f in get_extracted():
        fullpath = os.path.join(localsettings.outdir, f)
        hashcode = get_file_hash(f)
        entries.append((f, datetime.datetime.fromtimestamp(os.stat(fullpath).st_mtime), human_readable(os.stat(fullpath).st_size), hashcode))
    return sorted(entries, key=lambda i: i[0].lower())


def clear_rar_dir(folder):
    print "Attempt delete dir", folder
    for f in os.listdir(folder):
        if RARFILE.match(f):
            os.remove(os.path.join(folder, f))
            print "deleted", f
        else:
            print "not rar, will not delete", f
    os.rmdir(folder)
