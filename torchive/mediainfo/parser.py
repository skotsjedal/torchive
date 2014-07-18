from functions import functions
import reparse
from torchive.mediainfo import PATH

__author__ = 'Skotsj'

parser = reparse.parser(
    parser_type=reparse.alt_parser,
    expressions_yaml_path=PATH + 'expressions.yaml',
    patterns_yaml_path=PATH + 'patterns.yaml',
    functions=functions
)


def parse(filename):
    filename = filename.replace('_', ' ').replace(' ', '.')
    try:
        p = parser(filename)
        m = p[0][0]
        m.title = m.title.replace('.', ' ')
        return m
    except:
        raise Exception('Cannot parse %s' % filename)
