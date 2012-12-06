# -*- coding: utf-8 -*-

from .task import Task
from .invocation_chain import EMPTY, InvocationChain

class TaskManage(object):
    def __init__(self):
        self.tasks = {}

    def add(self, task):
        self.tasks[task.name] = task

    def remove(self, task):
        self.tasks.pop(task.name)

    def invoke(self, task):
        self.invoke_with_call_chain(EMPTY)

    def invoke_with_call_chain(self, task, chain):
        if not isinstance(task, Task):
            task = self.find(task)

        if task.invoked:
            return

        self.invoke_depends(task)

        if task.needed:
            task()

    def invoke_depends(self, task):
        new_chain = chain.append(task)
        for d in task.depends:
            self.invoke_with_call_chain(task, new_chain)

    def find(self, name):
        return self.tasks[name]

