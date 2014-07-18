import pickle
import os
from datetime import datetime
from objectcacher import cachefolder, Persisted, expire_threshold


def persist(obj):
    """

    Persist an object to cache

    :param obj: object to persist, object must have unique field ``id``
    """
    p = Persisted()
    p.id = obj.id
    p.type = obj.__class__.__name__
    p.obj = obj
    filename = get_filename(p.type, p.id)
    print 'saving object as %s' % filename
    with open(filename, 'wb') as f:
        pickle.dump(p, f)


def get_filename(objtype, idx):
    """
    internal helper method
    """
    filename = os.path.join(cachefolder, '%s_%d' % (objtype, idx))
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
    print 'loading object %s' % filename
    with open(filename, 'rb') as f:
        persisted = pickle.load(f)
        if (datetime.now() - persisted.time).seconds > expire_threshold:
            persisted.expired = True
        return persisted
