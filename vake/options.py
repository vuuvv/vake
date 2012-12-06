
class Options(dict):
    def __getattr__(self, name):
        val = self.get(name)
        if isinstance(val, Option):
            return val.value()
        raise AttributeError("Unrecongnized option %r" % name)

    def __setattr__(self, name, value):
        val = self.get(name)
        if isinstance(val, Option):
            return self[name].set(value)
        raise AttributeError("Unrecongnized option %r" % name)

class Option(object):
    def __init__(self, name, default=None, type=str, help=None,
                 metavar=None, multiple=False):
        if default is None and multiple:
            default = []
        self.name = name
        self.default = default
        self.type = type
        self.help = help
        self.metavar = metavar
        self.multiple = multiple

    def parse(self, value):
        parsers = {
            bool: self.parse_bool,
            str: self.parse_string,
        }
        parse = parsers.get(self.type, self.type)
        if self.multiple:
            _value = []
            for part in value.split(","):
                if self.type in (int, long):
                    lo, _, hi = part.partition(":")
                    lo = parse(lo)
                    hi = parse(hi) if hi else lo
                    _value.extend(range(lo, hi + 1))
                else:
                    _value.extend(parse(part))
        else:
            self._value = parse(value)
        return self.value()

    def value(self):
        return self.default if self._value is None else self._value

    def set(self, value):
        self._value = value

    def parse_bool(self, value):
        return value.lower() not in ("false", "0", "f")

    def parse_string(self, value):
        return str(value)

#options = Options()
#
#def define(*args, **kwargs):
#    options.define(*args, **kwargs)
