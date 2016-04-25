from .common import *
import ply.lex, ply.yacc

###########################################################
#                        PLY lex part
###########################################################

tokens = ('TokenNewline', 'TokenComment', 'TokenDelimiter', 'TokenLiteral')

class TokenNewline(Token):
    regex = r'(\r)?\n'

    @staticmethod
    def from_token(token):
        return TokenNewline()

class TokenComment(Token):
    regex = r'(^|(?<=\n))\;[^\r\n]*'

    def __init__(self, content):
        self.content = content

    @staticmethod
    def from_token(token):
        return TokenComment(token.value[1:])

    def __repr__(self):
        return '%s(%s)' % (self.__class__, repr(';' + self.content))
    
class TokenDelimiter(Token):
    regex = r'\:'

    @staticmethod
    def from_token(token):
        return TokenDelimiter()

class TokenLiteral(Token):
    regex = r'[^;:\r\n]+'

    def __init__(self, value):
        self.value = value

    @staticmethod
    def from_token(token):
        return TokenLiteral(token.value)

    def __repr__(self):
        return '%s(%s)' % (self.__class__, repr(self.value))

@ply.lex.TOKEN(TokenNewline.regex)
def t_TokenNewline(t):
    t.value = TokenNewline.from_token(t)
    return t

@ply.lex.TOKEN(TokenComment.regex)
def t_TokenComment(t):
    t.value = TokenComment.from_token(t)
    return t
            
@ply.lex.TOKEN(TokenDelimiter.regex)
def t_TokenDelimiter(t):
    t.value = TokenDelimiter.from_token(t)
    return t

@ply.lex.TOKEN(TokenLiteral.regex)
def t_TokenLiteral(t):
    t.value = TokenLiteral.from_token(t)
    return t

def t_error(t):
    raise LexerError(t, 'Encountered an illegal character.')

lexer = ply.lex.lex()
