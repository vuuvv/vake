# -*- coding: utf-8 -*-

from os import path as ospath
from time import time

def empty():
    pass

class Task(object):
    """
    task是vake系统中的核心组件。
    """
    def __init__(self, name, depends=[], action=empty, help=None):
        self.name = name
        self.depends = depends
        self.action = action
        self.help = help
        self.invoked = False

    def __call__(self, *args, **kwargs):
        self.action(self.name, self.depends, *args, **kwargs)
        self.invoked = True

    def __repr__(self):
        return '<Task %s => [%s]>' % (self.name,
                                      ",".join([d.name for d in self.depends]))

    def timestamp(self):
        time()

    def out_of_date(self):
        return False

    def needed(self):
        return True

class File(Task):
    def timestamp(self):
        return ospath.getmtime(self.name)

