###########################################################
#                   Exception definitions
###########################################################

class LexerError(SyntaxError):
    def __init__(self, t, message):
        super().__init__()
        self.filename = getattr(t.lexer, 'filename', None)
        self.lineno = t.lineno
        self.msg = message

class ParserError(SyntaxError):
    def __init__(self, p, message):
        super().__init__()
        self.filename = getattr(p.parser, 'filename', None)
        self.lineno = p.lineno(0)
        self.msg = message

###########################################################
#               Abstract token definition
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