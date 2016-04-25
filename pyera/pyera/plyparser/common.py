import ply

###########################################################
#                   Exception definitions
###########################################################

class LexerError(SyntaxError):
    def __init__(self, t, message):
        super().__init__()
        self.filename = getattr(t.lexer, 'filename', '<input>')
        self.lineno = t.lineno
        self.msg = message

class ParserError(SyntaxError):
    def __init__(self, p, message):
        super().__init__()
        if isinstance(p, ply.lex.LexToken):
            self.filename = getattr(p.lexer, 'filename', '<input>')
            self.lineno = p.lineno
        elif p == None:
            self.filename = '<input>'
            self.lineno = 0
        else:
            self.filename = getattr(p.parser, 'filename', '<input>')
            self.lineno = p.lineno(0)
        self.msg = message

###########################################################
#            Abstract token/symbol definition
###########################################################

class Token:
    #Tokens must hold valid values only.

    #the regex pattern for the token.
    regex = r''

    #Parse input token string to token object.
    #Raise an error if the token seems an invalid value. Otherwise return the parsed token object.
    @staticmethod
    def from_token(token):
        raise NotImplementedError

    #Optional, but recommended.
    def __repr__(self):
        return '%s()' % self.__class__

class Symbol:
    #Symbols must hold valid values only.

    #the regex pattern for the token.
    regex = r''

    #Parse input token string to token object.
    #Raise an error if the token seems an invalid value. Otherwise return the parsed token object.
    @staticmethod
    def from_token(token):
        raise NotImplementedError

    #Optional, but recommended.
    def __repr__(self):
        return '%s()' % type(self).__name__

###########################################################
#              Default warning/error handlers
###########################################################

def default_warning_handler(e):
    print('%s(%d): warning: %s' % (e.filename, e.lineno, e.msg))

def default_error_handler(e):
    print('%s(%d): error: %s' % (e.filename, e.lineno, e.msg))
    raise e