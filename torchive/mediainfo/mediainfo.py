import os
import shutil
from torchive.mediainfo import ImdbInfo, MediaInfo
from torchive.objectcacher import cacher, CACHEFOLDER

__author__ = 'Skotsj'
from imdb import IMDb
import json, requests

"""
I use omdbapi as imdbpy search function doesn't work
and vice versa as omdbapi doesn't provide season info for tv shows
"""
OMDBAPI_ENDP = 'http://www.omdbapi.com'

ia = IMDb(accessSystem='http', loggingLevel='debug')


def find(mediainfo):
    """

    :param mediainfo: Mediainfo object
    :return: ImdbInfo object
    """

    lookup_id = mediainfo.title
    imdbinfo_persist = cacher.try_get(ImdbInfo.__name__, lookup_id)
    if imdbinfo_persist is None or imdbinfo_persist.expired:
        imdbinfo = search_imdb(mediainfo.title, with_episodes=mediainfo.mtype == MediaInfo.TV)
        imdbinfo.id = mediainfo.title
        cacher.persist(imdbinfo)
    else:
        imdbinfo = imdbinfo_persist.obj

    return imdbinfo


def get_imdb_image(url):
    response = requests.get(url, stream=True)
    imagename = url[url.rindex('/')+1:]
    fullpathimage = os.path.join(CACHEFOLDER, imagename)
    with open(fullpathimage, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return imagename


def search_imdb(movie, with_episodes=False):
    """

    search imdb for info about a movie or tv show

    :param movie:
    :param with_episodes:
    :return:
    """
    # print 'searching for %s, with episodes:%s' % (movie, with_episodes)
    resp = requests.get(OMDBAPI_ENDP, params=dict(t=movie))
    respdict = json.loads(resp.text)
    del resp
    if not respdict['Response']:
        return None
    info = ImdbInfo()
    info.title = respdict['Title']
    info.imdbid = respdict['imdbID']
    info.image = get_imdb_image(respdict['Poster'])
    info.rating = respdict['imdbRating']
    info.year = respdict['Year']

    if not with_episodes:
        return info

    seasoninfo = get_seasons(info.imdbid)
    for season, seasondata in seasoninfo.iteritems():
        info.seasons[season] = len(seasondata)

    return info


def get_seasons(show_id):
    """
    Mainly to be used internally by find()

    :param show_id:
    :return:
    """
    if show_id.startswith('tt'):
        show_id = show_id[2:]
    # print 'searching for episodes of %s' % show_id
    return ia.get_movie_episodes(show_id)['data']['episodes']

