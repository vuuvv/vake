# -*- coding: utf-8 -*-

class InvocationChain(object):
    def __init__(self, value, tail):
        self.value = value
        self.tail = tail

    def __contains__(self, value):
        return self.value == value or value in self.tail

    def append(self, value):
        if value in self:
            raise RuntimeError("Circular dependency detected: %s => %s" % (
                self, value))
        return InvocationChain(value, self)

    def __repr__(self):
        return "%s%s" % (self.prefix, self.value)

    @property
    def prefix(self):
        return "%s => " % self.tail

class EmptyInvocationChain(object):
    def __contains__(self, value):
        return False

    def append(self, value):
        return InvocationChain(value, self)

    def __repr__(self):
        return "TOP"

EMPTY = EmptyInvocationChain()
