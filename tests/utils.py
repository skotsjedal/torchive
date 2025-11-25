import os
import sys
import types


def install_test_localsettings(base_dir, hash_salt="testsalt"):
    """Install an in-memory torchive.localsettings module for tests."""
    if "torchive" not in sys.modules:
        import torchive

    torchive_pkg = sys.modules["torchive"]
    module = types.ModuleType("torchive.localsettings")
    incoming = os.path.join(base_dir, "incoming") + os.sep
    outdir = os.path.join(base_dir, "out") + os.sep
    tmpdir = os.path.join(base_dir, "tmp") + os.sep
    donedir = os.path.join(base_dir, "done") + os.sep

    for folder in (incoming, outdir, tmpdir, donedir):
        os.makedirs(folder, exist_ok=True)

    module.BASEDIR = incoming
    module.OUTDIR = outdir
    module.TMPDIR = tmpdir
    module.DONEDIR = donedir

    module.USERNAME = "tester"
    module.PASSWORD = "secret"
    module.SECRET_KEY = "test-key"
    module.HASHSALT = hash_salt

    sys.modules[module.__name__] = module
    setattr(torchive_pkg, "localsettings", module)
    return module


def unload_localsettings():
    sys.modules.pop("torchive.localsettings", None)
    torchive_pkg = sys.modules.get("torchive")
    if torchive_pkg and hasattr(torchive_pkg, "localsettings"):
        delattr(torchive_pkg, "localsettings")
