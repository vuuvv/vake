import sys

def import_module(name, required=True):
    try:
        __import__(name, globals(), locals(), [])
    except ImportError:
        if not required:
            return None
        raise
    return sys.modules[name]

def import_attribute(name):
    path, attr = name.rsplit('.', 1)
    module = __import__(path, globals(), locals(), [attr])

    return getattr(module, attr)
