_locale = None

def setlocale(locale_module):
    global _locale
    _locale = locale_module

def _retrieve(s, v):
    def binsearch(b, e):
        if e - b == 0:
            return v
        m = (b + e) // 2
        mv, t = s[m]
        if isinstance(mv, list):
            mvb, mve = mv
            if v < mvb:
                return binsearch(b, m)
            elif v >= mve:
                return binsearch(m + 1, e)
            else:
                return t
        elif v < mv:
            return binsearch(b, m)
        elif v > mv:
            return binsearch(m + 1, e)
        else:
            return t
    return binsearch(0, len(s))

def tohalfwidth(string):
    ret = []
    for c in string:
        ret.append(chr(_retrieve(_locale.F2H, ord(c))))
    return ''.join(ret)

def tofullwidth(string):
    ret = []
    for c in string:
        ret.append(chr(_retrieve(_locale.H2F, ord(c))))
    return ''.join(ret)
