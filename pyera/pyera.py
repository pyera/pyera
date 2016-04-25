import sys
import os
import config


def main(rootpath):
    import plyparser.config
    pass

if __name__ == '__main__':
    try:
        rootpath = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.realpath(__file__))
    except NameError:
        rootpath = os.getcwd()
    main(rootpath)

