from mediainfo.parser import parse

import os
from torchive import localsettings


def test_livedata():
    for f in os.listdir(localsettings.OUTDIR):
        print parse(f)

