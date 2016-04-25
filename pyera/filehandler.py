import chardet
import io

def open(fn, write, codecname = 'mskanji', autodetect = 'safedetect'):
    if write or (autodetect == 'no'):
        return io.open(fn, {True: 'w', False: 'r'}[write], encoding=codecname)
    elif autodetect == 'chardet' or autodetect == 'mskanji' or autodetect == 'safedetect':
        with io.open(fn, 'rb') as f:
            buf = f.read()
        try:
            if autodetect == 'safedetect':
                #read only BOM and early characters.
                result = chardet.detect(buf[:10])
            else:
                result = chardet.detect(buf)
            confidence = result.get('confidence', 0.0)
            encoding = result.get('encoding', None)
            if encoding == None or confidence < 0.1:
                encoding = codecname
            elif encoding.upper().startswith('UTF-8'):
                encoding = 'utf-8-sig' #UTF-8 -> UTF-8-SIG (BOM)
            elif encoding.upper().startswith('UTF-16'):
                    encoding = 'UTF-16' #UTF-16LE -> UTF-16 (BOM)
            elif autodetect == 'safedetect':
                if not encoding.upper().startswith('UTF'):
                    encoding = codecname
            elif autodetect == 'mskanji' and encoding.upper() == 'SHIFT_JIS':
                encoding = 'mskanji'
        except:
            encoding = codecname

        file = io.BytesIO(buf)
        setattr(file, 'name', fn)

        return io.TextIOWrapper(file, encoding=encoding)
    else:
        raise LookupError(u'unknown autodetect mode: %s' % autodetect)

