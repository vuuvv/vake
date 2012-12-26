# -*- coding: utf-8 -*-

from os import path as ospath
from time import time

def empty():
    pass

class Task(object):
    """
    task是vake系统中的核心组件。
    """
    def __init__(self, name, depends=[], action=empty, help=None, parser=None):
        self._name = name
        self.depends = depends
        self.action = action
        self.help = help
        self.invoked = False
        self.parser = parser

    def __call__(self, argv=[]):
        args, argv = self.parser.parse_known_args(argv)
        kwargs = args.__dict__
        self.action(self, **kwargs)
        self.invoked = True

    def __repr__(self):
        return '<Task %s => [%s]>' % (
            self.name,
            ",".join([getattr(d, 'name', d) for d in self.depends])
        )

    def needed(self):
        return True

    @property
    def name(self):
        return self._name

class FileTask(Task):

    def needed(self):
        return (not self.exists()) or self._out_of_date()

    @property
    def name(self):
        return 'file:%s' % self._name

    def _out_of_date(self):
        return any([self._out_than(dep) for dep in self.depends])

    def _out_than(self, other):
        if not isinstance(other, FileTask) or not other.exists():
            return True
        return ospath.getmtime(self._name) < ospath.getmtime(other._name)

    def exists(self):
        return ospath.exists(self._name)

    @staticmethod
    def is_file_task(name):
        return name.startswith("file:")

