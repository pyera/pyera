import typing
import enum
import ply.lex, ply.yacc
from .common import *
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
    t.lexer.lineno += 1
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
    error(LexerError.from_token(t, 'Encountered an illegal character.'))

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
        warning(ParserError.from_symbol(p, "Ignoring values after the second ':' for setting '%s'." % k))
    p[0] = (k, v)
    
def p_error(t):
    warning(ParserError.from_token(t, 'Unexpected %s' % (t.value if t else 'EOF')))

# Build the parser
parser = ply.yacc.yacc()

###########################################################
#         Value parser and Config object generator
###########################################################

def set_config_entry_value(configentry, v):
    if configentry.fixed:
        warning(ParserError(parser.filename, 0, 'Tried to overwrite a fixed configuration.'))
        return False
    if v == '':
        warning(ParserError(parser.filename, 0, 'The configuration value is an empty string.'))
        return False
    v = v.strip()
    if configentry.dtype == bool:
        try:
            configentry.value = (int(dtype) != 0)
            return True
        except:
            pass
        if v in ('NO', 'FALSE', '後'):
            configentry.value = False
            return True
        elif v in ('YES', 'TRUE', '前'):
            configentry.value = True
            return True
        else:
            raise ValueError
    if configentry.dtype == config.Color:
        rgb = v.split(',')
        if len(rgb) < 3:
            raise ValueError
        elif len(rgb) > 3:
            warning(ParserError(parser.filename, 0, 'The value of configuration %s (\'%s\') has more than 3 entries. Truncating.' % (k, v)))
            rgb = rgb[:3]
        rgb = tuple(int(i) for i in rgb)
        for i in rgb:
            if not (0 <= i <= 255):
                raise ValueError
        configentry.value = config.Color(r = rgb[0], g = rgb[1], b = rgb[2])
        return True
    elif configentry.dtype == config.char:
        if len(v) != 1:
            return False
        configentry.value = v
        return True
    elif configentry.dtype == int:
        configentry.value = int(v)
        return True
    elif configentry.dtype == str:
        configentry.value = v
        return True
    elif configentry.dtype == typing.List[int]:
        #Bug in Emuera1821: it will set the value to the point where parse is successful.
        configentry.value = []
        for segment in v.split('/'):
            configentry.value.append(int(segment.strip()))
        return True
    elif type(configentry.dtype) == enum.EnumMeta:
        configentry.value = configentry.dtype[v]
        return True
    else:
        raise RuntimeError('Cannot reach here')

#Config object generater, based on parsed result
def parse(input, cfg = None, fixed = False):
    parsed = parser.parse(input)
    ret = cfg or config.Config.get_default_config()
    for k, v in parsed:
        if k == ':comment':
            continue
        canonical_k = T_(k, 'config')
        if canonical_k == 'CompatiDRAWLINE':
            warning(ParserError(parser.filename, 0, 'CompatiDRAWLINE is deprecated. Use CompatiLinefeedAs1739.'))
            canonical_k = 'CompatiLinefeedAs1739'
        if canonical_k not in ret:
            warning(ParserError(parser.filename, 0, 'Configuration %s does not exist.' % k))
            continue
        if canonical_k == 'EditorArgument':
            #Bug in Emuera1821: it never fixates the EditorArgument even if it is set from csv/_fixed.config
            #We'll simulate this bug for compatibility reason. We'll not support this option in the application anyway.
            ret[canonical_k].value = v
        else:
            try:
                if(set_config_entry_value(ret[canonical_k], v)):
                    ret[canonical_k].fixed = fixed
            except ValueError as e:
                warning(ParserError(parser.filename, 0, 'The value of configuration %s (\'%s\') cannot be understood. We will use configuration only up to this point.' % (k, v)))
                break
    ret.parsed_config_files = [(parser.filename, parsed)]
    return ret