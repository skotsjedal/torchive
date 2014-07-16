from functions import functions
import reparse

__author__ = 'Skotsj'

path = ""
if '__file__' in globals():
    import os

    path = str(os.path.dirname(__file__))
    if path:
        path += "/"

parser = reparse.parser(
    parser_type=reparse.alt_parser,
    expressions_yaml_path=path + 'expressions.yaml',
    patterns_yaml_path=path + 'patterns.yaml',
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
