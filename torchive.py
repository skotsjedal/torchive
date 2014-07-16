#!/usr/bin/python
from enzyme import MalformedMKVError
from flask import Flask, render_template, jsonify
import localsettings
from core.core import get_dirs, get_all, get_all_out, get_file_hash, RARTEMP
from mediainfo.parser import parse
from mkvinfo.mkvinfo import Mkvinfo
from rar.rar import Rar
from rarfile import RarFile
import datetime
from werkzeug.wrappers import Response
from functools import wraps
from flask import request
from shutil import copy2, rmtree
import os


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == localsettings.username and password == localsettings.password


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


DEBUG = True
SECRET_KEY = localsettings.secret_key
USERNAME = localsettings.username
PASSWORD = localsettings.password

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
    return render_template('down.html', entries=entries)


@app.route('/x/<entry>/<path:name>')
@requires_auth
def extract(entry, name):
    rfile = RarFile(localsettings.basedir + name)
    start = datetime.datetime.now().replace(microsecond=0)
    try:
        extdir = localsettings.outdir
        if entry[-4:] == ".rar":
            extdir = localsettings.basedir + RARTEMP
        rfile.extract(entry, path=extdir)
        print name, "extracted"
    except:
        status = 'failed'
        print name, "failed extract"
        response = jsonify(status=status)
        response.status_code = 400
        return response
    time = str(datetime.datetime.now().replace(microsecond=0) - start)
    return jsonify(time=time, file=entry, status='success')


@app.route('/s/<path:name>')
@requires_auth
def stream(name):
    return Response(file(localsettings.outdir + name), direct_passthrough=True)

@app.route('/hs/<hashcode>/<path:name>')
def hash_stream(hashcode, name):
    hashcode_i = get_file_hash(name)
    print hashcode, hashcode_i
    if hashcode != hashcode_i:
        response = jsonify(status='error', error='wrong hash')
        response.status_code = 401
        return response

    return Response(file(localsettings.outdir + name), direct_passthrough=True)


@app.route('/c/<path:name>')
@requires_auth
def copy(name):
    filename = name[name.rindex("/") + 1:] if '/' in name else name
    fullpath = os.path.join(localsettings.basedir, name)
    target = os.path.join(localsettings.outdir, filename)
    start = datetime.datetime.now().replace(microsecond=0)
    try:
        if os.path.isdir(fullpath):
            for ff in os.listdir(fullpath):
                fullpath_f = os.path.join(fullpath, ff)
                target_f = os.path.join(localsettings.outdir, ff)
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
    time = str(datetime.datetime.now().replace(microsecond=0) - start)
    return jsonify(time=time, file=filename, status='success')


@app.route('/m/<path:name>')
@requires_auth
def move(name):
    fullpath = os.path.join(localsettings.outdir, name)
    target = os.path.join(localsettings.donedir, name)
    start = datetime.datetime.now().replace(microsecond=0)
    try:
        os.rename(fullpath, target)
        print name, "moved"
    except Exception, e:
        status = 'failed'
        response = jsonify(status, error=str(e))
        response.status_code = 400
        print name, "move failed"
        return response
    time = str(datetime.datetime.now().replace(microsecond=0) - start)
    return jsonify(time=time, file=name, status='success')


@app.route('/d/<path:name>')
@requires_auth
def delete(name):
    fullpath = os.path.join(localsettings.basedir, name)
    try:
        if os.path.isdir(fullpath):
            rmtree(fullpath)
            print name, "deleted dir"
        else:
            os.remove(fullpath)
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
    fullpath = os.path.join(localsettings.outdir, name)
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
    fullpath = os.path.join(localsettings.outdir, name)
    try:
        mkvinfo = Mkvinfo(fullpath)
    except MalformedMKVError, e:
        response = jsonify(status='failed', error=str(e))
        response.status_code = 400
        return response
    return render_template('_partial/fileInfo.html', mkvinfo=mkvinfo.all)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
