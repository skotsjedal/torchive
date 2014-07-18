import os
from mediainfo import MediaInfo
from objectcacher import cachefolder
from objectcacher.cacher import persist, try_get
from shutil import rmtree

__author__ = 'skotsj'

info = MediaInfo()
info.id = 123
info.title = 'Te silly ones'


def testcleanup():
    if os.path.exists(cachefolder):
        rmtree(cachefolder)
    os.mkdir(cachefolder)


def testsave():
    persist(info)


def testload():
    info_loaded = try_get(MediaInfo.__name__, info.id)
    assert info_loaded is not None
    assert info_loaded.id == info.id
    assert info_loaded.title == info.title
