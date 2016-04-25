import unittest
import pprint
from .plyparser import parse, config

class TestConfig(unittest.TestCase):
    def test_config(self):
        '''Config parser test. Must show two warnings.'''
        parse_result = parse(config,
r'''大文字小文字の違いを無視する:YES
_Rename.csvを利用する:YES
_Replace.csvを利用する:YES
マウスを使用する:YES
メニューを使用する:YES
デバッグコマンドを使用する:YES
多重起動を許可する:NO
オートセーブを行なう:YES
キーボードマクロを使用する:YES
ウィンドウの高さを可変にする:YES
描画インターフェース:WINAPI
ウィンドウ幅:1200
ウィンドウ高さ:900
ウィンドウ位置X:21
ウィンドウ位置Y:31
起動時のウィンドウ位置を指定する:YES
起動時にウィンドウを最大化する:NO
履歴ログの行数:5000
PRINTCを並べる数:3
PRINTCの文字数:25
フォント名:ＭＳ ゴシック
フォントサイズ:18
一行の高さ:19
文字色:192,192,192
背景色:0,0,0
選択中文字色:255,255,0
履歴文字色:192,192,192
フレーム毎秒:5
最大スキップフレーム数:3
スクロール行数:1
無限ループ警告までのミリ秒数:5000
表示する最低警告レベル:0
ロード時にレポートを表示する:NO
ロード時に引数を解析する:YES
呼び出されなかった関数を無視する:NO
関数が見つからない警告の扱い:DISPLAY
関数が呼び出されなかった警告の扱い:IGNORE
ボタンの途中で行を折りかえさない:YES
サブディレクトリを検索する:YES
読み込み順をファイル名順にソートする:YES
表示するセーブデータ数:20
eramaker互換性に関する警告を表示する:NO
システム関数の上書きを許可する:YES
システム関数が上書きされたとき警告を表示する:YES
関連づけるテキストエディタ:notepad:test1:test2:test3
テキストエディタコマンドライン指定:USER_SETTING
エディタに渡す行指定引数:
同名の非イベント関数が複数定義されたとき警告する:NO
解釈不可能な行があっても実行する:NO
CALLNAMEが空文字列の時にNAMEを代入する:NO
セーブデータをsavフォルダ内に作成する:YES
擬似変数RANDの仕様をeramakerに合わせる:NO
関数・属性については大文字小文字を無視しない:NO
全角スペースをホワイトスペースに含める:NO
セーブデータをUTF-8で保存する:YES
ver1739以前の非ボタン折り返しを再現する:NO
内部で使用する東アジア言語:KOREAN
ONEINPUT系命令でマウスによる2文字以上の入力を許可する:NO
イベント関数のCALLを許可する:NO
SPキャラを使用する:NO
セーブデータをバイナリ形式で保存する:NO
ユーザー関数の全ての引数の省略を許可する:YES
ユーザー関数の引数に自動的にTOSTRを補完する:YES
FORM中の三連記号を展開しない:NO
TIMESの計算をeramakerにあわせる:NO
;comment test
no_config_test:test_value
illformed test (warning here)
''')
        reference = (
'''{'AllowFunctionOverloading': ConfigEntry<bool>(AllowFunctionOverloading, False),
 'AllowLongInputByMouse': ConfigEntry<bool>(AllowLongInputByMouse, False),
 'AllowMultipleInstances': ConfigEntry<bool>(AllowMultipleInstances, False),
 'AutoSave': ConfigEntry<bool>(AutoSave, False),
 'BackColor': ConfigEntry<Color>(BackColor, Color(r=0, g=0, b=0)),
 'ButtonWrap': ConfigEntry<bool>(ButtonWrap, False),
 'ChangeMasterNameIfDebug': ConfigEntry<bool>(ChangeMasterNameIfDebug, True),
 'CompatiCALLNAME': ConfigEntry<bool>(CompatiCALLNAME, False),
 'CompatiCallEvent': ConfigEntry<bool>(CompatiCallEvent, False),
 'CompatiDRAWLINE': ConfigEntry<bool>(CompatiDRAWLINE, False),
 'CompatiErrorLine': ConfigEntry<bool>(CompatiErrorLine, False),
 'CompatiFuncArgAutoConvert': ConfigEntry<bool>(CompatiFuncArgAutoConvert, False),
 'CompatiFuncArgOptional': ConfigEntry<bool>(CompatiFuncArgOptional, False),
 'CompatiFunctionNoignoreCase': ConfigEntry<bool>(CompatiFunctionNoignoreCase, False),
 'CompatiLinefeedAs1739': ConfigEntry<bool>(CompatiLinefeedAs1739, False),
 'CompatiRAND': ConfigEntry<bool>(CompatiRAND, False),
 'CompatiSPChara': ConfigEntry<bool>(CompatiSPChara, False),
 'DisplayReport': ConfigEntry<bool>(DisplayReport, False),
 'DisplayWarningLevel': ConfigEntry<int>(DisplayWarningLevel, 1),
 'EditorArgument': ConfigEntry<str>(EditorArgument, ''),
 'EditorType': ConfigEntry<TextEditorType>(EditorType, <TextEditorType.USER_SETTING: 4>),
 'FPS': ConfigEntry<int>(FPS, 5),
 'FocusColor': ConfigEntry<Color>(FocusColor, Color(r=255, g=255, b=0)),
 'FontName': ConfigEntry<str>(FontName, 'ＭＳ ゴシック'),
 'FontSize': ConfigEntry<int>(FontSize, 18),
 'ForeColor': ConfigEntry<Color>(ForeColor, Color(r=192, g=192, b=192)),
 'FunctionNotCalledWarning': ConfigEntry<DisplayWarningFlag>(FunctionNotCalledWarning, <DisplayWarningFlag.IGNORE: 1>),
 'FunctionNotFoundWarning': ConfigEntry<DisplayWarningFlag>(FunctionNotFoundWarning, <DisplayWarningFlag.DISPLAY: 4>),
 'IgnoreCase': ConfigEntry<bool>(IgnoreCase, False),
 'IgnoreUncalledFunction': ConfigEntry<bool>(IgnoreUncalledFunction, False),
 'InfiniteLoopAlertTime': ConfigEntry<int>(InfiniteLoopAlertTime, 5000),
 'LastKey': ConfigEntry<int>(LastKey, 0),
 'LineHeight': ConfigEntry<int>(LineHeight, 19),
 'LogColor': ConfigEntry<Color>(LogColor, Color(r=192, g=192, b=192)),
 'MaxLog': ConfigEntry<int>(MaxLog, 5000),
 'PrintCLength': ConfigEntry<int>(PrintCLength, 25),
 'PrintCPerLine': ConfigEntry<int>(PrintCPerLine, 3),
 'ReduceArgumentOnLoad': ConfigEntry<ReduceArgumentOnLoadFlag>(ReduceArgumentOnLoad, <ReduceArgumentOnLoadFlag.YES: 1>),
 'SaveDataNos': ConfigEntry<int>(SaveDataNos, 20),
 'ScrollHeight': ConfigEntry<int>(ScrollHeight, 1),
 'SearchSubdirectory': ConfigEntry<bool>(SearchSubdirectory, False),
 'SetWindowPos': ConfigEntry<bool>(SetWindowPos, False),
 'SizableWindow': ConfigEntry<bool>(SizableWindow, False),
 'SkipFrame': ConfigEntry<int>(SkipFrame, 3),
 'SortWithFilename': ConfigEntry<bool>(SortWithFilename, False),
 'SystemAllowFullSpace': ConfigEntry<bool>(SystemAllowFullSpace, False),
 'SystemIgnoreTripleSymbol': ConfigEntry<bool>(SystemIgnoreTripleSymbol, False),
 'SystemNoTarget': ConfigEntry<bool>(SystemNoTarget, False),
 'SystemSaveInBinary': ConfigEntry<bool>(SystemSaveInBinary, False),
 'SystemSaveInUTF8': ConfigEntry<bool>(SystemSaveInUTF8, False),
 'TextDrawingMode': ConfigEntry<TextDrawingMode>(TextDrawingMode, <TextDrawingMode.WINAPI: 3>),
 'TextEditor': ConfigEntry<str>(TextEditor, 'notepad'),
 'TimesNotRigorousCalculation': ConfigEntry<bool>(TimesNotRigorousCalculation, False),
 'UseDebugCommand': ConfigEntry<bool>(UseDebugCommand, False),
 'UseKeyMacro': ConfigEntry<bool>(UseKeyMacro, False),
 'UseMenu': ConfigEntry<bool>(UseMenu, False),
 'UseMouse': ConfigEntry<bool>(UseMouse, False),
 'UseRenameFile': ConfigEntry<bool>(UseRenameFile, False),
 'UseReplaceFile': ConfigEntry<bool>(UseReplaceFile, False),
 'UseSaveFolder': ConfigEntry<bool>(UseSaveFolder, False),
 'WarnBackCompatibility': ConfigEntry<bool>(WarnBackCompatibility, False),
 'WarnFunctionOverloading': ConfigEntry<bool>(WarnFunctionOverloading, False),
 'WarnNormalFunctionOverloading': ConfigEntry<bool>(WarnNormalFunctionOverloading, False),
 'WindowMaximixed': ConfigEntry<bool>(WindowMaximixed, False),
 'WindowPosX': ConfigEntry<int>(WindowPosX, 0),
 'WindowPosY': ConfigEntry<int>(WindowPosY, 0),
 'WindowX': ConfigEntry<int>(WindowX, 760),
 'WindowY': ConfigEntry<int>(WindowY, 480),
 'useLanguage': ConfigEntry<UseLanguage>(useLanguage, <UseLanguage.KOREAN: 2>)}''')
        self.assertEqual(pprint.pformat(parse_result,indent=1, width=80), reference)


if __name__ == '__main__':
    unittest.main()
