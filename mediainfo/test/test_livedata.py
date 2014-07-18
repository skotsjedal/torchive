from mediainfo.parser import parse
import localsettings
import os


def test_livedata():
    for f in os.listdir(localsettings.outdir):
        print parse(f)

