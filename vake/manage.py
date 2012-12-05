from .task import Task
from .invocation_chain import EMPTY, InvocationChain

class TaskManage(object):
    def __init__(self):
        self.tasks = {}

    def add(self, task):
        pass

    def remove(self, task):
        pass

    def invoke(self, task):
        self.invoke_with_call_chain(EMPTY)

    def invoke_with_call_chain(self, task, chain):
        if not isinstance(task, Task):
            task = self.find(task)

        if task.invoked:
            return

        new_chain = chain.append(task)

        for d in task.depends:
            self.invoke_with_call_chain(task, new_chain)

        if task.needed:
            task()

    def find(self, name):
        return self.tasks[name]

