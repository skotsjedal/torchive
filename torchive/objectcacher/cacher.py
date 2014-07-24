import pickle
import os
from datetime import datetime
from torchive.objectcacher import CACHEFOLDER, Persisted, EXPIRE_THRESHOLD


def persist(obj):
    """

    Persist an object to cache

    :param obj: object to persisted, object must have unique field ``id``
    """
    persisted = Persisted()
    persisted.id = obj.id
    persisted.type = obj.__class__.__name__
    persisted.obj = obj
    filename = get_filename(persisted.type, persisted.id)
    #print 'saving object as %s' % filename
    with open(filename, 'wb') as persist_file:
        pickle.dump(persisted, persist_file)


def get_filename(objtype, idx):
    """
    internal helper method
    """
    idx = str(idx).replace(' ', '.').lower()
    filename = os.path.join(CACHEFOLDER, '%s_%s.pkl' % (objtype, idx))
    return filename


def try_get(objtype, idx):
    """

    try to get an object

    :param objtype: string, class of object, you can use <object>.__class__.__name__
    :param idx: index of object to get
    :return: a Persisted object or None if it was not found
    """
    filename = get_filename(objtype, idx)
    if not os.path.exists(filename):
        print 'couldn\'t find file %s' % filename
        return None
    #print 'loading object %s' % filename
    with open(filename, 'rb') as persist_file:
        persisted = pickle.load(persist_file)
        age = datetime.now() - persisted.time
        if age > EXPIRE_THRESHOLD:
            persisted.expired = True
        return persisted
