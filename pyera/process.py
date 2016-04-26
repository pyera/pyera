import os
import pprint
from . import filehandler
from . import plyparser
from . import config
from . import locale

def warning(msg):
    print('warning: %s' % msg)

class Process:
    def __init__(self, rootpath):
        self.rootpath = rootpath
        self.savdir = self.rootpath
        
        self._load_config()
        self._setlocale()
        
        
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
        #set runtime configurations
        self.config.runtime_config['CaseInsensitiveFunctions'] = self.config('IgnoreCase') and not self.config('CompatiFunctionNoignoreCase')
        self.config.runtime_config['CaseInsensitiveVariables'] = self.config('IgnoreCase')

        if self.config('AllowFunctionOverloading') and not self.config('WarnFunctionOverloading'):
            self.config.runtime_config['WarnFunctionOverloading'] = True
        
        if self.config('FontSize') < 8:
            warning('font size is clamped up to 8.')
            self.config.runtime_config['FontSize'] = 8
        if self.config('LineHeight') < self.config('FontSize'):
            warning('line height is clamped up to %d (font size).' % self.config('FontSize'))
            self.config.runtime_config['LineHeight'] = self.config('FontSize')
        if self.config('SaveDataNos') < 20:
            warning('number of save data is clamped up to 20.')
            self.config.runtime_config['SaveDataNos'] = 20
        elif self.config('SaveDataNos') > 80:
            warning('number of save data is clamped down to 80.')
            self.config.runtime_config['SaveDataNos'] = 80
        if self.config('MaxLog') < 500:
            warning('maximum number of log lines is clamped up to 500.')
            self.config.runtime_config['MaxLog'] = 500
        
        self.savdir = self.path('sav') if self.config('UseSaveFolder') else self.rootpath
        #We'll not support automatic save folder migration.

        #TODO: Change ReduceArgumentOnLoad if needed (refer MinorShift.Emuera.ConfigData.LoadConfig() line 417-423)
        #Original analysis note: ReduceArgumentOnLoad가
        #-> ONCE이고 ERB/CSB가 최근에 바뀌었거나 emuera.config가 없었다면 새로 생성해서 저장.
        #-> ON이면 NeedReduceArgumentOnLoad = true 세팅. emuera.config가 없었다면 새로 생성해서 저장.
        #-> OFF면 NeedReduceArgumentOnLoad = false 세팅. emuera.config가 없었다면 새로 생성해서 저장.
        #-> TODO: 왠지는 분석요망.

    def _setlocale(self):
        if self.config('useLanguage') == config.UseLanguage['JAPANESE']:
            from .locale import ja_JP
            locale.setlocale(ja_JP)
        elif self.config('useLanguage') == config.UseLanguage['KOREAN']:
            from .locale import ko_KR
            locale.setlocale(ko_KR)
        elif self.config('useLanguage') == config.UseLanguage['CHINESE_HANS']:
            from .locale import zh_HANS
            locale.setlocale(zh_HANS)
        else: #self.config('useLanguage') == config.UseLanguage['CHINESE_HANT']:
            from .locale import zh_HANT
            locale.setlocale(zh_HANT)

    def path(self, *arg, none_if_nonexists = True):
        ret = os.path.join(self.rootpath, *arg)
        if none_if_nonexists and not os.path.exists(ret):
            return None
        return ret
