import unittest
from .plyparser import parse, config

class TestConfig(unittest.TestCase):
    def test_config(self):
        parse_result = parse(config,
r''';comment test 1
大文字小文字の違いを無視する:YES
illformed line
;
;comment test 2
;
invalid-comment1:;1
invalid-comment2:;
:;3
関連づけるテキストエディタ:notepad:abc:def:ghi
エディタに渡す行指定引数:test xxxx:yyyy

;comment test 3
SPキャラを使用する:NO

''')
        reference = (
            (':comment', 'comment test 1'),
            ('大文字小文字の違いを無視する', 'YES'),
            (':comment', ''),
            (':comment', 'comment test 2'),
            (':comment', ''),
            ('invalid-comment1', ';1'),
            ('invalid-comment2', ';'),
            ('関連づけるテキストエディタ', 'notepad:def:ghi'),
            ('エディタに渡す行指定引数', 'test xxxx'),
            (':comment', 'comment test 3'),
            ('SPキャラを使用する', 'NO'))
        self.assertEqual(parse_result, reference)


if __name__ == '__main__':
    unittest.main()
