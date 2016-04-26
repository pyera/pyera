import os
import pprint
from . import filehandler
from . import plyparser

class Process:
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self._load_config()
        #pprint.pprint(self.config)
        
    def _load_config(self):
        self.config = None
        def add_config(fn, fixed):
            if fn == None:
                return
            with filehandler.open(fn, False) as f:
                self.config = plyparser.parse(plyparser.config_file, f.read(), fn, cfg = self.config, fixed = fixed)
        add_config(self.path('csv','_default.config') or self.path('csv','default.config'), False)
        add_config(self.path('emuera.config'), False)
        add_config(self.path('csv','_fixed.config') or self.path('csv','fixed.config'), True)
        
    def path(self, *arg, none_if_nonexists = True):
        ret = os.path.join(self.rootpath, *arg)
        if none_if_nonexists and not os.path.exists(ret):
            return None
        return ret
