from datetime import datetime
import os
from shutil import copy2, rmtree
from os import remove, rename, path, listdir
import traceback

from enzyme import MalformedMKVError
from flask import Flask, render_template, jsonify, send_file, request
from rarfile import RarFile
import sys
from werkzeug.wrappers import Response

from torchive import localsettings
from torchive.auth import requires_auth
from torchive.core.core import get_dirs, get_all, get_all_out, RARTEMP, get_file_hash
from torchive.mediainfo import mediainfo
from torchive.mediainfo.parser import parse
from torchive.mkvinfo.mkvinfo import Mkvinfo
from torchive.objectcacher import CACHEFOLDER
from torchive.rar.rar import Rar


DEBUG = True
SECRET_KEY = localsettings.SECRET_KEY
USERNAME = localsettings.USERNAME
PASSWORD = localsettings.PASSWORD

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
@requires_auth
def index():
    rars = [Rar(d) for d in get_dirs()]
    return render_template('index.html', rars=rars)


@app.route('/list/')
@requires_auth
def list_all():
    entries = get_all()
    return render_template('list.html', entries=entries)


@app.route('/outlist/')
@requires_auth
def list_all_out():
    entries = get_all_out()
    # TODO try out more VLC protocol
    return render_template('down.html', entries=entries, host=request.host, protocol='http')


def stream(name):
    filename = os.path.join(localsettings.OUTDIR, name)

    def stream_movie():
        with open(filename, "rb") as f:
            byte_s = f.read(512)
            while byte_s:
                yield byte_s
                byte_s = f.read(512)

    t = os.stat(filename)

    sz = str(t.st_size)
    return Response(stream_movie(), mimetype='video/x-matroska',
                    headers={"Content-Type": "video/x-matroska", "Content-Disposition": "inline",
                             "Content-Transfer-Enconding": "binary", "Content-Length": sz})


@app.route('/s/<path:name>')
@requires_auth
def protected_stream(name):
    return stream(name)


@app.route('/hs/<hashcode>/<path:name>')
def hash_stream(hashcode, name):
    hashcode_i = get_file_hash(name)
    print hashcode, hashcode_i
    if hashcode != hashcode_i:
        response = jsonify(status='error', error='wrong hash')
        response.status_code = 401
        return response

    return stream(name)


@app.route('/x/<entry>/<path:name>')
@requires_auth
def extract(entry, name):
    rfile = RarFile(localsettings.BASEDIR + name)
    start = datetime.now().replace(microsecond=0)
    try:
        extdir = localsettings.OUTDIR
        if entry[-4:] == ".rar":
            extdir = localsettings.BASEDIR + RARTEMP
        rfile.extract(entry, path=extdir)
        print name, "extracted"
    except:
        status = 'failed'
        print name, "failed extract"
        response = jsonify(status=status)
        response.status_code = 400
        return response
    time = str(datetime.now().replace(microsecond=0) - start)
    return jsonify(time=time, file=entry, status='success')


@app.route('/c/<path:name>')
@requires_auth
def copy(name):
    filename = name[name.rindex("/") + 1:] if '/' in name else name
    fullpath = path.join(localsettings.BASEDIR, name)
    target = path.join(localsettings.OUTDIR, filename)
    start = datetime.now().replace(microsecond=0)
    try:
        if path.isdir(fullpath):
            for ff in listdir(fullpath):
                fullpath_f = path.join(fullpath, ff)
                target_f = path.join(localsettings.OUTDIR, ff)
                copy2(fullpath_f, target_f)
                print ff, "copied"
        else:
            copy2(fullpath, target)
            print name, "copied"
    except Exception, e:
        status = 'failed'
        print name, "failed copy"
        response = jsonify(status=status, error=str(e))
        response.status_code = 400
        return response
    time = str(datetime.now().replace(microsecond=0) - start)
    return jsonify(time=time, file=filename, status='success')


@app.route('/m/<path:name>')
@requires_auth
def move(name):
    fullpath = path.join(localsettings.OUTDIR, name)
    target = path.join(localsettings.DONEDIR, name)
    start = datetime.now().replace(microsecond=0)
    try:
        rename(fullpath, target)
        print name, "moved"
    except Exception, e:
        status = 'failed'
        response = jsonify(status, error=str(e))
        response.status_code = 400
        print name, "move failed"
        return response
    time = str(datetime.now().replace(microsecond=0) - start)
    return jsonify(time=time, file=name, status='success')


@app.route('/d/<path:name>')
@requires_auth
def delete(name):
    fullpath = path.join(localsettings.BASEDIR, name)
    try:
        if path.isdir(fullpath):
            rmtree(fullpath)
            print name, "deleted dir"
        else:
            remove(fullpath)
            print name, "deleted single file"
    except OSError, e:
        status = 'failed'
        response = jsonify(status=status, error=str(e))
        response.status_code = 400
        print name, "delete failed"
        return response
    return jsonify(status='success')


@app.route('/i/<path:name>')
@requires_auth
def get_track_info(name):
    fullpath = path.join(localsettings.OUTDIR, name)
    status = 'success'
    try:
        mkvinfo = Mkvinfo(fullpath)
    except MalformedMKVError, e:
        status = 'error'
        mkvinfo = e
    try:
        info = parse(name).__dict__
    except:
        info = None

    return jsonify(status=status, info=mkvinfo.all_json, filenameinfo=info)


@app.route('/ih/<path:name>')
@requires_auth
def get_track_info_html(name):
    print name
    fullpath = path.join(localsettings.OUTDIR, name)
    try:
        mkvinfo = Mkvinfo(fullpath)
    except MalformedMKVError, e:
        response = jsonify(status='failed', error=str(e))
        response.status_code = 400
        return response
    return render_template('_partial/fileInfo.html', mkvinfo=mkvinfo.all)


@app.route('/mi/<path:name>')
@requires_auth
def get_mediainfo(name):
    try:
        minfo = parse(name)
        imdbinfo = mediainfo.find(minfo)
    except Exception, e:
        print "Exception:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        response = jsonify(status='failed', error=str(e))
        response.status_code = 500
        return response

    print imdbinfo
    return render_template('_partial/mediaInfo.html', imdbinfo=imdbinfo)


@app.route('/imdbimg/<image>')
@requires_auth
def get_image(image):
    image = os.path.join(CACHEFOLDER, image)
    if os.path.exists(image):
        return send_file(image, mimetype='image/jpg')

    response = jsonify(status='failed')
    response.status_code = 404
    return response

