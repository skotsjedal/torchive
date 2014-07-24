from datetime import datetime, timedelta
import os

PATH = ''
if '__file__' in globals():
    PATH = str(os.path.dirname(__file__))
    if PATH:
        PATH += '/'

CACHEFOLDER = PATH + 'cache'
EXPIRE_THRESHOLD = timedelta(days=7)

if not os.path.exists(CACHEFOLDER):
    os.mkdir(CACHEFOLDER)


class Persisted:
    def __init__(self):
        self.id = None
        self.type = None
        self.time = datetime.now()
        self.obj = None
        self.expired = False
