from .task import Task

class TaskDecorator(object):
    def __init__(self, depends=[], name=None, default=False, help=None):
        self.depends = depends
        self.name = name
        self.default = default
        self.help = help

    def __call__(self, func):
        name = self.name or func.__name__
        task = Task(self.name, self.depends, func, help)
