from flask import Flask, render_template
import localsettings
from rar.rar import Rar
import os

DEBUG = True
SECRET_KEY = localsettings.secret_key
USERNAME = localsettings.username
PASSWORD = localsettings.password

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def hello_world():
    rootentries = [os.path.join(localsettings.basedir, f) for f in os.listdir(localsettings.basedir)]
    rars = []
    for e in rootentries:
        if os.path.isdir(e):
            rars.append(Rar(e))
    print len(rars)
    #print rars
    for rarfile in rars:
        #print rarfile.folder_name
        for a in rarfile.archives:
            #print a.name
            print len(a.files)
            #for f in a.files:
            #    print f.name
    return render_template('index.html', rars=rars)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
