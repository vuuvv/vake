from .task import Task
from .manage import TaskManage

from vake import app

class TaskDecorator(object):
    def __init__(self, depends=[], name=None, default=False, help=None):
        self.depends = depends
        self.name = name
        self.default = default
        self.help = help
        self.options = []

    def __call__(self, func):
        if isinstance(func, OptionDecorator):
            self.options = func.options
            func = func.func

        self.name = self.name or func.__name__
        self.help = func.__doc__ if func.__doc__ else self.name

        parser = self._args_parse()

        task = Task(self.name, self.depends, func, help, parser)
        app.add_task(task)
        return self

    def _args_parse(self):
        parser = app.subparser.add_parser(self.name, help=self.help)
        for args, kwargs in self.options:
            parser.add_argument(*args, **kwargs)
        return parser

def task(*args, **kwargs):
    return TaskDecorator(*args, **kwargs)

class OptionDecorator(object):
    def __init__(self, *args, **kwargs):
        self.options = [(args, kwargs)]

    def __call__(self, func):
        if isinstance(func, OptionDecorator):
            self.options += func.options
        self.func = func
        return self

def option(*args, **kwargs):
    return OptionDecorator(*args, **kwargs)
