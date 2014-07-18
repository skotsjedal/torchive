import os
from mediainfo import MediaInfo
from objectcacher import CACHEFOLDER
from objectcacher.cacher import persist, try_get
from shutil import rmtree

__author__ = 'skotsj'

info = MediaInfo()
info.id = 123
info.title = 'Te silly ones'


def testcleanup():
    if os.path.exists(CACHEFOLDER):
        rmtree(CACHEFOLDER)
    os.mkdir(CACHEFOLDER)


def testsave():
    global info
    persist(info)


def testload():
    global info
    persisted = try_get(MediaInfo.__name__, info.id)
    assert persisted is not None
    assert not persisted.expired
    info_loaded = persisted.obj
    assert info_loaded is not None
    assert info_loaded.id == info.id
    assert info_loaded.title == info.title
