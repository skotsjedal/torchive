import importlib
import os
import pickle
import sys
import tempfile
import unittest
from datetime import datetime, timedelta


class DummyObject:
    def __init__(self, idx, title):
        self.id = idx
        self.title = title


class ObjectCacherTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_dir = self.temp_dir.name

        # Ensure a clean module import using the temporary cache folder
        if "torchive.objectcacher" in sys.modules:
            del sys.modules["torchive.objectcacher"]
        if "torchive.objectcacher.cacher" in sys.modules:
            del sys.modules["torchive.objectcacher.cacher"]

        self.oc = importlib.import_module("torchive.objectcacher")
        self.oc.CACHEFOLDER = self.cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cacher = importlib.import_module("torchive.objectcacher.cacher")
        self.cacher.CACHEFOLDER = self.cache_dir

    def tearDown(self):
        self.temp_dir.cleanup()
        for module in ["torchive.objectcacher", "torchive.objectcacher.cacher"]:
            if module in sys.modules:
                del sys.modules[module]

    def test_persist_and_try_get_roundtrip(self):
        sample = DummyObject(7, "demo")
        self.cacher.persist(sample)

        persisted = self.cacher.try_get(DummyObject.__name__, sample.id)
        self.assertIsNotNone(persisted)
        self.assertFalse(persisted.expired)
        self.assertEqual(persisted.obj.id, sample.id)
        self.assertEqual(persisted.obj.title, sample.title)

    def test_expired_object_is_flagged(self):
        sample = DummyObject(8, "old")
        persisted = self.oc.Persisted()
        persisted.id = sample.id
        persisted.type = sample.__class__.__name__
        persisted.obj = sample
        persisted.time = datetime.now() - self.oc.EXPIRE_THRESHOLD - timedelta(hours=1)

        filename = self.cacher.get_filename(persisted.type, persisted.id)
        with open(filename, "wb") as persist_file:
            pickle.dump(persisted, persist_file)

        loaded = self.cacher.try_get(persisted.type, persisted.id)
        self.assertIsNotNone(loaded)
        self.assertTrue(loaded.expired)


if __name__ == "__main__":
    unittest.main()
