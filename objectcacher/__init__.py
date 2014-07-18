from datetime import datetime
import os

path = ''
if '__file__' in globals():
    path = str(os.path.dirname(__file__))
    if path:
        path += '/'

cachefolder = path + 'cache'
expire_threshold = 2 * 3600  # hours to seconds

if not os.path.exists(cachefolder):
    os.mkdir(cachefolder)


class Persisted:
    def __init__(self):
        self.id = None
        self.type = None
        self.time = datetime.now()
        self.obj = None
        self.expired = False
