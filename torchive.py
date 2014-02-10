from flask import Flask, render_template, jsonify
import localsettings
from core.core import get_dirs, get_all, get_all_out, RARTEMP
from rar.rar import Rar
from rarfile import RarFile
import datetime
from werkzeug.wrappers import Response
from functools import wraps
from flask import request
from shutil import copy2
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
    rfile = RarFile(localsettings.basedir+name)
    start = datetime.datetime.now().replace(microsecond=0)
    status = 'success'
    try:
        extdir = localsettings.outdir
        if entry[-4:] == ".rar":
            extdir = localsettings.basedir+RARTEMP
        rfile.extract(entry, path=extdir)
    except:
        status = 'failed'
    time = str(datetime.datetime.now().replace(microsecond=0)-start)
    return jsonify(time=time, file=entry, status=status)


@app.route('/s/<path:name>')
@requires_auth
def stream(name):
    return Response(file(localsettings.outdir + name), direct_passthrough=True)


@app.route('/c/<path:name>')
@requires_auth
def copy(name):
    filename = name[name.rindex("/")+1:] if '/' in name else name
    fullpath = os.path.join(localsettings.basedir, name)
    target = os.path.join(localsettings.outdir, filename)
    start = datetime.datetime.now().replace(microsecond=0)
    status = 'success'
    try:
        copy2(fullpath, target)
    except:
        status = 'failed'
    time = str(datetime.datetime.now().replace(microsecond=0)-start)
    return jsonify(time=time, file=filename, status=status)


@app.route('/m/<path:name>')
@requires_auth
def move(name):
    fullpath = os.path.join(localsettings.outdir, name)
    target = os.path.join(localsettings.donedir, name)
    start = datetime.datetime.now().replace(microsecond=0)
    status = 'success'
    try:
        os.rename(fullpath, target)
    except:
        status = 'failed'
    time = str(datetime.datetime.now().replace(microsecond=0)-start)
    return jsonify(time=time, file=name, status=status)


@app.route('/d/<path:name>')
@requires_auth
def delete(name):
    fullpath = os.path.join(localsettings.basedir, name)
    status = 'success'
    try:
        os.remove(fullpath)
    except:
        status = 'failed'
    return jsonify(status=status)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
