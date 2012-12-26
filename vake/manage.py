# -*- coding: utf-8 -*-

from .task import Task
from .invocation_chain import EMPTY, InvocationChain

class DuplicatedTaskName(Exception):
    pass

class TaskNotFound(Exception):
    pass

class TaskManage(object):
    def __init__(self):
        self.tasks = {}
        self._default = 'all'

    def add(self, task, default=False):
        if task.name in self.tasks:
            raise DuplicatedTaskName("Duplication task name: '%s'" % task.name)
        self.tasks[task.name] = task
        if default:
            self._default = task.name

    def remove(self, task):
        if isinstance(task, Task):
            self.tasks.pop(task.name)
        self.tasks.pop(task)

    def invoke(self, task):
        if not isinstance(task, Task):
            task = self.find(task)
        self.invoke_with_call_chain(task, EMPTY)

    def invoke_with_call_chain(self, task, chain):
        if not isinstance(task, Task):
            task = self.find(task)

        if task.invoked:
            return

        self.invoke_depends(task, chain)

        if task.needed():
            task()

    def invoke_depends(self, task, chain):
        new_chain = chain.append(task)
        for d in task.depends:
            self.invoke_with_call_chain(d, new_chain)

    def find(self, name):
        try:
            return self.tasks[name]
        except KeyError:
            raise TaskNotFound("Can't find task: '%s'" % name)

    @property
    def default(self):
        try:
            return self.find(self._default)
        except TaskNotFound:
            return None

