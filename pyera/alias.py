ALIAS_MAP = { 'global': {} }

def register(name, value, namespace = 'global'):
    if namespace not in ALIAS_MAP:
        ALIAS_MAP[namespace] = {}
    elif name in ALIAS_MAP:
        raise KeyError('Registering alias for %s::%s failed: already exists.' % (namespace, name))
    ALIAS_MAP[namespace][name] = value

def T_(name, namespace = 'global'):
   if namespace in ALIAS_MAP:
       return ALIAS_MAP[namespace].get(name, name)
   return name
