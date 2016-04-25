import unittest
import plyparser.config

class TestConfig(unittest.TestCase):
    def test_lex(self):
        plyparser.config.lexer.input(
''';comment test 1
大文字小文字の違いを無視する:YES
キーボードマクロを使用する:YES
illformed line
;
;comment test 2
;
関連づけるテキストエディタ:notepad
エディタに渡す行指定引数:test xxxx:yyyy

;comment test 3
SPキャラを使用する:NO

''')
        types = (plyparser.config.TokenComment, plyparser.config.TokenNewline,
             plyparser.config.TokenLiteral, plyparser.config.TokenDelimiter, plyparser.config.TokenLiteral, plyparser.config.TokenNewline,
             plyparser.config.TokenLiteral, plyparser.config.TokenDelimiter, plyparser.config.TokenLiteral, plyparser.config.TokenNewline,
             plyparser.config.TokenLiteral, plyparser.config.TokenNewline,
             plyparser.config.TokenComment, plyparser.config.TokenNewline,
             plyparser.config.TokenComment, plyparser.config.TokenNewline,
             plyparser.config.TokenComment, plyparser.config.TokenNewline,
             plyparser.config.TokenLiteral, plyparser.config.TokenDelimiter, plyparser.config.TokenLiteral, plyparser.config.TokenNewline,
             plyparser.config.TokenLiteral, plyparser.config.TokenDelimiter, plyparser.config.TokenLiteral, plyparser.config.TokenDelimiter, plyparser.config.TokenLiteral, plyparser.config.TokenNewline,
             plyparser.config.TokenNewline,
             plyparser.config.TokenComment, plyparser.config.TokenNewline,
             plyparser.config.TokenLiteral, plyparser.config.TokenDelimiter, plyparser.config.TokenLiteral, plyparser.config.TokenNewline,
             plyparser.config.TokenNewline)

        for i, token in enumerate(plyparser.config.lexer):
            self.assertIsInstance(token.value, types[i])

if __name__ == '__main__':
    unittest.main()
