import ply.lex, ply.yacc
import numpy

##############################
#    Exception Definitions
##############################

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


##############################
#        PLY lex part
##############################

tokens = ('TokenIntegerLiteral',)

class Token:
    #Tokens must hold valid values only.

    #the regex pattern for the token.
    regex = r''

    #Parse input token string to token object.
    #Raise an error if the token seems an invalid value. Otherwise return the parsed token object.
    
    @staticmethod
    def from_token(token):
        r''
        raise NotImplementedError
    
class TokenIntegerLiteral(Token):
    #64-bit integer. Parsed at MinorShift.Emuera.Sub.LexicalAnalyzer.ReadInt64(StringStream st, bool retZero)
    # ** This parser is compliant only for when retZero == false. 
    # ** The only case of retZero == true is when string-to-int internal functions are called. ( TOINT() and ISNUMERIC() )
    # ** These can be exceptionally handled.

    regex = r'(0[xX][\+\-]?[0-9a-fA-F]+([pPeE][\+\-]?[0-9a-fA-F]+)?)|(0[bB][\+\-]?[0-9]+([pPeE][\+\-]?[0-9]+)?)|([\+\-]?[0-9]+([pPeE][\+\-]?[0-9]+)?)'

    #e.g., a number "0x+000Fe+0A" is interpreted as following:
    # "  0x     +         000F           e         +          0A     "
    #  [base] [sign] [number_string] [expbase] [expsign] [exp_string]
    #base: One of 2, 10, 16 (octal number is not supported in Emuera)
    #sign: '-' if negation sign is provided, '+' if positive sign is explicitly provided, '' otherwise
    #      Cannot be '-' if base != 10
    #number_string: literal value
    #expbase: One of 0, 2, 10 (0 if exponent part is not specified at all)
    #expsign: '-' if negation sign is provided, '+' if positive sign is explicitly provided, '' otherwise
    #      Cannot be '-' if base != 10
    #expnumber_string: literal value of exponent
    def __init__(self, base, sign, number_string, expbase, expsign, expnumber_string):
        super().__init__()
        self.base = base
        self.sign = sign
        self.number_string = number_string
        self.expbase = expbase
        self.expsign = expsign
        self.expnumber_string = expnumber_string

    @staticmethod
    def from_token(token):
        s = token.value
        
        #base extraction
        base_string = s[:2]
        if base_string in ('0x', '0X'):
            base = 16
            s = s[2:]
        elif base_string in ('0b', '0B'):
            base = 2
            s = s[2:]
        else:
            base = 10

        def read_segment():
            #sign extraction
            nonlocal s
            sign = ''
            if s[0] in ('+', '-'):
                sign = s[0]
                if base != 10 and sign == '-': #System.Convert.ToInt64 behavior
                    raise LexerError(token, 'Negative integer notation is not supported for non-decimals.')
                s = s[1:]
            #number_string extraction
            i = 0
            while i < len(s) and s[i] in {2: '0123456789', 10: '0123456789', 16: '0123456789abcdefABCDEF'}[base]:
                #Emuera takes 2-9 in binary numbers as well, but throw errors instead.
                if base == 2 and s[i] in '23456789':
                    raise LexerError(token, 'Invalid digit in base 2 numbers.')
                i += 1
            number_string = s[:i]
            s = s[i:]
            return sign, number_string
        
        sign, number_string = read_segment()

        #expbase extraction
        if len(s) == 0:
            expbase, expsign, expnumber_string = 0, '', ''
        elif s[0] in ('p', 'P'):
            expbase = 2
            s = s[1:]
            expsign, expnumber_string = read_segment()
        else: #s[0] in ('e', 'E'):
            expbase = 10
            s = s[1:]
            expsign, expnumber_string = read_segment()
        try:
            ret = TokenIntegerLiteral(base, sign, number_string, expbase, expsign, expnumber_string)
            ret.value() #check if it is within 64 bit integer range
            return ret
        except:
            raise LexerError(token, 'Cannot interpret as 64 bit integer.')

    def value(self):
        n = int(self.sign + self.number_string, base=self.base)
        if self.expbase != 0:
            e = int(self.expsign + self.expnumber_string, base=self.base)
            n = n * (self.expbase ** e)
        return numpy.int64(n)
            
@ply.lex.TOKEN(TokenIntegerLiteral.regex)
def t_TokenIntegerLiteral(t):
    t.value = TokenIntegerLiteral.from_token(t)
    return t

def t_error(t):
    raise LexerError(t, 'Encountered an illegal character.')

if __name__ == '__main__':
    lexer = ply.lex.lex()
    lexer.input('0x+FFFCp+4 a')
    print(lexer.token().value.value())

