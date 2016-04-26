import sys
import os
import unittest
import pprint
import codecs

import pyera
import pyera.filehandler
import pyera.unittest
import pyera.plyparser
import pyera.plyparser.config_file

def main(rootpath):
    if sys.stdout.encoding not in ('utf-8', 'utf8'):
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    unittest.main(module = 'pyera.unittest', argv = [sys.argv[0]], testRunner = unittest.TextTestRunner(stream = sys.stdout))


if __name__ == '__main__':
    try:
        rootpath = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.realpath(__file__))
    except NameError:
        rootpath = os.getcwd()
    main(rootpath)

