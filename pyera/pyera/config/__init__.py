import enum
import collections
import typing
import copy
from . import localization
from .. import filehandler
from .. import plyparser


###########################################################
#              Entry value type definitions
###########################################################

Color = collections.namedtuple('Color', ['r', 'g', 'b'])
TextDrawingMode = enum.Enum('TextDrawingMode', ('GRAPHICS', 'TEXTRENDERER', 'WINAPI'))
ReduceArgumentOnLoadFlag = enum.Enum('ReduceArgumentOnLoadFlag', ('YES', 'ONCE', 'NO'))
DisplayWarningFlag = enum.Enum('DisplayWarningFlag', ('IGNORE', 'LATER', 'ONCE', 'DISPLAY'))
TextEditorType = enum.Enum('TextEditorType', ('SAKURA', 'TERAPAD', 'EMEDITOR', 'USER_SETTING'))
UseLanguage = enum.Enum('UseLanguage', ('JAPANESE', 'KOREAN', 'CHINESE_HANS', 'CHINESE_HANT'))

class char(str):
    pass

class ConfigEntry:
    def __init__(self, code, dtype, value, fixed = False):
        self.code = code
        self.dtype = dtype
        self.value = value
        self.fixed = fixed
    def __repr__(self):
        return '%s<%s>(%s, %s%s)' % (type(self).__name__, self.dtype.__name__, self.code, repr(self.value), '*' if self.fixed else '')

###########################################################
#                    Entry definitions
###########################################################

#refer to MinorShift.Emuera.ConfigData.setDefault(); we won't differentiate between configArray and replaceArray.
CONFIG_DEFAULT = (
	ConfigEntry('IgnoreCase', bool, True),
	ConfigEntry('UseRenameFile', bool, False),
	ConfigEntry('UseReplaceFile', bool, True),
	ConfigEntry('UseMouse', bool, True),
	ConfigEntry('UseMenu', bool, True),
	ConfigEntry('UseDebugCommand', bool, False),
	ConfigEntry('AllowMultipleInstances', bool, True),
	ConfigEntry('AutoSave', bool, True),
	ConfigEntry('UseKeyMacro', bool, True),
	ConfigEntry('SizableWindow', bool, True),
    ConfigEntry('TextDrawingMode', TextDrawingMode, TextDrawingMode['GRAPHICS']),
    ConfigEntry('WindowX', int, 760),
	ConfigEntry('WindowY', int, 480),
	ConfigEntry('WindowPosX', int, 0),
	ConfigEntry('WindowPosY', int, 0),
	ConfigEntry('SetWindowPos', bool, False),
	ConfigEntry('WindowMaximixed', bool, False),
	ConfigEntry('MaxLog', int, 5000),
	ConfigEntry('PrintCPerLine', int, 3),
	ConfigEntry('PrintCLength', int, 25),
	ConfigEntry('FontName', str, 'ＭＳ ゴシック'),
	ConfigEntry('FontSize', int, 18),
	ConfigEntry('LineHeight', int, 19),
	ConfigEntry('ForeColor', Color, Color(192, 192, 192)),
	ConfigEntry('BackColor', Color, Color(0, 0, 0)),
	ConfigEntry('FocusColor', Color, Color(255, 255, 0)),
	ConfigEntry('LogColor', Color, Color(192, 192, 192)),
	ConfigEntry('FPS', int, 5),
	ConfigEntry('SkipFrame', int, 3),
	ConfigEntry('ScrollHeight', int, 1),
	ConfigEntry('InfiniteLoopAlertTime', int, 5000),
	ConfigEntry('DisplayWarningLevel', int, 1),
	ConfigEntry('DisplayReport', bool, False),
	ConfigEntry('ReduceArgumentOnLoad', ReduceArgumentOnLoadFlag, ReduceArgumentOnLoadFlag['NO']),
    ConfigEntry('IgnoreUncalledFunction', bool, True),
	ConfigEntry('FunctionNotFoundWarning', DisplayWarningFlag, DisplayWarningFlag['IGNORE']),
	ConfigEntry('FunctionNotCalledWarning', DisplayWarningFlag, DisplayWarningFlag['IGNORE']),
	ConfigEntry('ChangeMasterNameIfDebug', bool, True),
	ConfigEntry('ButtonWrap', bool, False),
	ConfigEntry('SearchSubdirectory', bool, False),
	ConfigEntry('SortWithFilename', bool, False),
	ConfigEntry('LastKey', int, 0),
	ConfigEntry('SaveDataNos', int, 20),
	ConfigEntry('WarnBackCompatibility', bool, True),
	ConfigEntry('AllowFunctionOverloading', bool, True),
	ConfigEntry('WarnFunctionOverloading', bool, True),
	ConfigEntry('TextEditor', str, 'notepad'),
	ConfigEntry('EditorType', TextEditorType, TextEditorType['USER_SETTING']),
	ConfigEntry('EditorArgument', str, ''),
	ConfigEntry('WarnNormalFunctionOverloading', bool, False),
	ConfigEntry('CompatiErrorLine', bool, False),
	ConfigEntry('CompatiCALLNAME', bool, False),
	ConfigEntry('UseSaveFolder', bool, False),
	ConfigEntry('CompatiRAND', bool, False),
	ConfigEntry('CompatiDRAWLINE', bool, False),
	ConfigEntry('CompatiFunctionNoignoreCase', bool, False),
	ConfigEntry('SystemAllowFullSpace', bool, True),
	ConfigEntry('SystemSaveInUTF8', bool, False),
	ConfigEntry('CompatiLinefeedAs1739', bool, False),
	ConfigEntry('useLanguage', UseLanguage, UseLanguage['JAPANESE']),
	ConfigEntry('AllowLongInputByMouse', bool, False),
	ConfigEntry('CompatiCallEvent', bool, False),
	ConfigEntry('CompatiSPChara', bool, False),
	ConfigEntry('SystemSaveInBinary', bool, False),
	ConfigEntry('CompatiFuncArgOptional', bool, False),
	ConfigEntry('CompatiFuncArgAutoConvert', bool, False),
	ConfigEntry('SystemIgnoreTripleSymbol', bool, False),
	ConfigEntry('TimesNotRigorousCalculation', bool, False),
    ConfigEntry('SystemNoTarget', bool, False)
)
REPLACE_CONFIG_DEFAULT = (
    ConfigEntry('MoneyLabel', str, '$'),
	ConfigEntry('MoneyFirst', bool, True),
	ConfigEntry('LoadLabel', str, 'Now Loading...'),
	ConfigEntry('MaxShopItem', int, 100),
	ConfigEntry('DrawLineString', str, '-'),
	ConfigEntry('BarChar1', char, '*'),
	ConfigEntry('BarChar2', char, '.'),
	ConfigEntry('TitleMenuString0', str, '最初からはじめる'),
	ConfigEntry('TitleMenuString1', str, 'ロードしてはじめる'),
	ConfigEntry('ComAbleDefault', int, 1),
	ConfigEntry('StainDefault', typing.List[int], [0, 0, 2, 1, 8]),
	ConfigEntry('TimeupLabel', str, '時間切れ'),
	ConfigEntry('ExpLvDef', typing.List[int], [0, 1, 4, 20, 50, 200]),
	ConfigEntry('PalamLvDef', typing.List[int], [0, 100, 500, 3000, 10000, 30000, 60000, 100000, 150000, 250000]),
	ConfigEntry('pbandDef', int, 4),
	ConfigEntry('RelationDef', int, 0)
)

class Config(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #list of (filename, parsed_raw_data) tuple
        self.parsed_config_files = []
    @staticmethod
    def get_default_config():
        ret = Config()
        for entry in CONFIG_DEFAULT:
            ret[entry.code] = copy.copy(entry)
        return ret
    @staticmethod
    def get_default_replace_config():
        ret = Config()
        for entry in REPLACE_CONFIG_DEFAULT:
            ret[entry.code] = copy.copy(entry)
        return ret
    