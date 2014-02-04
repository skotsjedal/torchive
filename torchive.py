from flask import Flask, render_template, jsonify
import localsettings
from core.core import get_dirs
from rar.rar import Rar
from rarfile import RarFile
import datetime
from werkzeug.wrappers import Response

DEBUG = True
SECRET_KEY = localsettings.secret_key
USERNAME = localsettings.username
PASSWORD = localsettings.password

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def hello_world():
    rars = [Rar(d) for d in get_dirs()]
    return render_template('index.html', rars=rars)


@app.route('/x/<path:name>')
def extract(name):
    file = RarFile(localsettings.basedir+name)
    start = datetime.datetime.now().replace(microsecond=0)
    status = 'success'
    try:
        file.extractall(path=localsettings.outdir)
    except:
        status = 'failed'
    time = str(datetime.datetime.now().replace(microsecond=0)-start)
    return jsonify(time=time, files=file.infolist().__len__(), status=status)


@app.route('/s/<path:name>')
def stream(name):
    return Response(file(localsettings.outdir + name), direct_passthrough=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
