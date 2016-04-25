import sys
import os
import pyera.unittest
import unittest
import pprint
import codecs

def main(rootpath):
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    import pyera.unittest
    unittest.main(module='pyera.unittest', argv=[sys.argv[0]])

if __name__ == '__main__':
    try:
        rootpath = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.realpath(__file__))
    except NameError:
        rootpath = os.getcwd()
    main(rootpath)

