import hashlib
import importlib
import os
import sys
import tempfile
import unittest

from tests.utils import install_test_localsettings, unload_localsettings


class CoreHashingTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.localsettings = install_test_localsettings(self.temp_dir.name, hash_salt="pepper")
        # Reload modules so they pick up the test localsettings
        if "torchive.core.core" in sys.modules:
            del sys.modules["torchive.core.core"]
        self.core = importlib.import_module("torchive.core.core")

    def tearDown(self):
        self.temp_dir.cleanup()
        unload_localsettings()
        if "torchive.core.core" in sys.modules:
            del sys.modules["torchive.core.core"]

    def test_hashfolder_handles_unicode_and_slashes(self):
        path = "shows/år/episode01"
        expected_parts = []
        partial = ""
        for folder in path.split("/"):
            partial += "/" + folder
            digest = hashlib.sha1(partial.encode("utf-8")).hexdigest()[:12]
            expected_parts.append(digest)
        expected = " ".join(expected_parts)

        self.assertEqual(expected, self.core.hashfolder(path))

    def test_get_file_hash_matches_manual_digest(self):
        filename = "movie.mkv"
        filepath = os.path.join(self.localsettings.OUTDIR, filename)
        with open(filepath, "wb") as handle:
            handle.write(b"payload")

        expected = hashlib.sha1(
            (filename + str(os.path.getsize(filepath)) + self.localsettings.HASHSALT).encode("utf-8")
        ).hexdigest()[:12]

        self.assertEqual(expected, self.core.get_file_hash(filename))

    def test_get_all_lists_files_with_sizes(self):
        folder = os.path.join(self.localsettings.BASEDIR, "series")
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, "episode.mkv")
        with open(filepath, "wb") as handle:
            handle.write(b"\x00" * 2048)

        entries = self.core.get_all()
        matching = [entry for entry in entries if entry[2] == "episode.mkv"]
        self.assertEqual(len(matching), 1)
        depth, itemname, name, size, extracted, done, idx = matching[0]
        self.assertEqual(depth, 1)
        self.assertEqual(itemname, "series/episode.mkv")
        self.assertEqual(size, self.core.human_readable(2048))
        self.assertFalse(extracted)
        self.assertFalse(done)
        self.assertEqual(len(idx.split(" ")), len(itemname.split("/")))


if __name__ == "__main__":
    unittest.main()
