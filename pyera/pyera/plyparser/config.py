from .common import *
import ply.lex, ply.yacc
from .. import config
from ..alias import T_

warning = default_warning_handler
error = default_error_handler

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
        return '%s(%s)' % (type(self).__name__, repr(self.content))
    
class TokenDelimiter(Token):
    regex = r'\:'

    @staticmethod
    def from_token(token):
        return TokenDelimiter()

class TokenLiteral(Token):
    regex = r'[^:\r\n]+'

    def __init__(self, value):
        self.value = value

    @staticmethod
    def from_token(token):
        return TokenLiteral(token.value)

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, repr(self.value))

@ply.lex.TOKEN(TokenNewline.regex)
def t_TokenNewline(t):
    t.value = TokenNewline.from_token(t)
    t.lineno += 1
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
    error(LexerError(t, 'Encountered an illegal character.'))

lexer = ply.lex.lex()

###########################################################
#                      PLY yacc part
###########################################################

def p_SymbolConfig_minimal(p):
    r'''SymbolConfig : SymbolLine'''
    p[0] = (p[1],) if p[1] else ()

def p_SymbolConfig_additional(p):
    r'''SymbolConfig : SymbolConfig TokenNewline SymbolLine'''
    p[0] = p[1] + (p[3],) if p[3] else p[1]

def p_SymbolLine_comment(p):
    r'''SymbolLine : TokenComment'''

    #track comments as we need it in reconstruction later
    p[0] = (':comment', p[1].content)

def p_SymbolLine_emptyline(p):
    r'''SymbolLine :'''
    p[0] = None

def p_SymbolLine_error(p):
    r'''SymbolLine : error'''
    p[0] = None

def p_SymbolLine_wellformed(p):
    r'''SymbolLine : SymbolLineWellformed'''
    k, v = p[1]
    #special treat for 'TextEditor'; see MinorShift.Emuera.ConfigData.loadConfig() line 464
    if k[0] == ':':
        k = k[1:]
    p[0] = (k, v)

def p_SymbolLineWellformed_minimal(p):
    r'''SymbolLineWellformed : TokenLiteral TokenDelimiter
                             | TokenLiteral TokenDelimiter TokenLiteral'''
    k = p[1].value.strip()
    v = '' if len(p) == 3 else p[3].value
    #special treat for 'TextEditor'; see MinorShift.Emuera.ConfigData.loadConfig() line 464
    if T_(k, 'config') == 'TextEditor':
        k = ':' + k
    p[0] = k, v

def p_SymbolLineWellformed_additional(p):
    r'''SymbolLineWellformed : SymbolLineWellformed TokenDelimiter
                             | SymbolLineWellformed TokenDelimiter TokenLiteral'''
    k, v = p[1]
    #special treat for 'TextEditor'; see MinorShift.Emuera.ConfigData.loadConfig() line 464
    if k[0] == ':': 
        k = k[1:]
        if len(p) == 4 and p[3].value[0] == '\\':
            v += ':' + p[3].value
    elif T_(k, 'config') == 'TextEditor':
        v += ':' + ('' if len(p) == 3 else p[3].value)
    else:
        warning(ParserError(p, "Ignoring values after the second ':' for setting '%s'." % k))
    p[0] = (k, v)
    
def p_error(t):
    warning(ParserError(t, 'Unexpected %s' % (t.value if t else 'EOF')))

# Build the parser
parser = ply.yacc.yacc()
