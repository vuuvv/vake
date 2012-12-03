# -*- coding: utf-8 -*-

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

    def __call__(self, *args, **kwargs):
        if not self.out_of_date():
            self.action(self.name, self.depends, *args, **kwargs)

    def __repr__(self):
        return '<Task %s => [%s]>' % (self.name,
                                      ",".join([d.name for d in self.depends]))

    def out_of_date(self):
        return False

class File(Task):
    pass

