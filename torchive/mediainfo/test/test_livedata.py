from torchive.mediainfo.parser import parse

import os
from torchive import localsettings


def ignore_test_livedata():
    """

    Test for development work only

    :return:
    """
    for f in os.listdir(localsettings.OUTDIR):
        print parse(f)

