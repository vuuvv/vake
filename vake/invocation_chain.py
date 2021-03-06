# -*- coding: utf-8 -*-

class EmptyInvocationChain(object):
    def __contains__(self, value):
        return False

    def append(self, value):
        return InvocationChain(value, self)

    def __repr__(self):
        return "TOP"

EMPTY = EmptyInvocationChain()

class InvocationChain(object):
    """
    专门用来检测循环依赖的类，由于层级不会太高，所以不考虑效率问题.
    """
    def __init__(self, value, tail=EMPTY):
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

