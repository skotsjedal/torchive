import torchive.localsettings
from os import remove, path, rmdir, listdir, stat
from re import compile
from datetime import datetime
from hashlib import sha1

RARTEMP = u'InnerArchs'
RARFILE = compile('.*\.r(\d\d|ar)')


def hashfolder(string):
    digests = []
    folders = string.split('/')
    partial = ''
    for f in folders:
        partial += '/'+f.encode('utf-8')
        h = sha1(partial)
        hexd = h.hexdigest()[0:12]
        digests.append(hexd)
    fullhex = ' '.join(digests)
    print string, fullhex
    return fullhex


def get_file_hash(name):
    fsize = stat(torchive.localsettings.OUTDIR + name).st_size
    hashbase = name + str(fsize) + torchive.localsettings.HASHSALT
    return sha1(hashbase).hexdigest()[0:12]


def get_dirs():
    rootentries = [path.join(torchive.localsettings.BASEDIR, f) for f in listdir(torchive.localsettings.BASEDIR)]
    dirs = []
    for e in rootentries:
        if path.isdir(e):
            dirs.append(e)
    return dirs


def get_done():
    return listdir(torchive.localsettings.DONEDIR)

def get_extracted():
    return listdir(torchive.localsettings.OUTDIR)


def get_downloading():
    return listdir(torchive.localsettings.TMPDIR)


def get_inner_archs():
    return listdir(torchive.localsettings.BASEDIR+RARTEMP)


def human_readable(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def get_all(depth=0, folder=torchive.localsettings.BASEDIR):
    entries = []
    if isinstance(folder, str):
        folder = unicode(folder, 'UTF-8')
    for f in listdir(folder):
        foldername = folder[folder.rindex('/')+1:]
        if not RARTEMP == foldername and RARFILE.match(f):
            continue
        entry = path.join(folder, f)
        itemname = entry[len(torchive.localsettings.BASEDIR):]
        idx = hashfolder(itemname)
        if path.isdir(entry):
            if not f == RARTEMP:
                entries.append((depth, itemname, f, "Directory", False, False, idx))
            entries += get_all(depth+1, entry)
        else:
            extracted = f in get_extracted()
            entries.append((depth, itemname, f, human_readable(stat(entry).st_size), extracted, f in get_done(), idx))
    entries = sorted(entries, key=lambda i: i[1].lower())
    return entries


def get_all_out():
    entries = []
    for f in get_extracted():
        fullpath = path.join(torchive.localsettings.OUTDIR, f)
        hashcode = get_file_hash(f)
        entries.append((f, datetime.fromtimestamp(stat(fullpath).st_mtime), human_readable(stat(fullpath).st_size), hashcode))
    return sorted(entries, key=lambda i: i[0].lower())


def clear_rar_dir(folder):
    print "Attempt delete dir", folder
    for f in listdir(folder):
        if RARFILE.match(f):
            remove(path.join(folder, f))
            print "deleted", f
        else:
            print "not rar, will not delete", f
    rmdir(folder)
