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
    m = parser(filename)
    try:
      m = m[0][0]
      return m
    except:
      print filename
      print m
      raise Exception
    m.title = m.title.replace('.', ' ')
    return m
