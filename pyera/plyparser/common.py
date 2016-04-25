import ply

###########################################################
#                   Exception definitions
###########################################################

class LexerError(SyntaxError):
    def __init__(self, filename, lineno, message):
        super().__init__()
        self.filename = filename
        self.lineno = lineno
        self.msg = message
    @staticmethod
    def from_token(t, message):
        return LexerError(getattr(t.lexer, 'filename', '<input>'), t.lineno, message)


class ParserError(SyntaxError):
    def __init__(self, filename, lineno, message):
        super().__init__()
        self.filename = filename
        self.lineno = lineno
        self.msg = message
    @staticmethod
    def from_token(t, message):
        if t == None:
            return ParserError('<input>', 0, message)
        return ParserError(getattr(t.lexer, 'filename', '<input>'), t.lineno, message)
    @staticmethod
    def from_symbol(p, message):
        if p == None:
            return ParserError('<input>', 0, message)
        return ParserError(getattr(p.parser, 'filename', '<input>'), p.lineno(0), message)
    
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
        return '%s' % type(self).__name__

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
        return '%s' % type(self).__name__

###########################################################
#              Default warning/error handlers
###########################################################

def default_warning_handler(e):
    if e.lineno == 0:
        print('%s: warning: %s' % (e.filename, e.msg))
    else:
        print('%s(%d): warning: %s' % (e.filename, e.lineno, e.msg))

def default_error_handler(e):
    if e.lineno == 0:
        print('%s: error: %s' % (e.filename, e.msg))
    else:
        print('%s(%d): error: %s' % (e.filename, e.lineno, e.msg))
    raise e
