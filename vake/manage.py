from .task import Task

class TaskManage(object):
    def __init__(self):
        self.tasks = {}

    def add(self, task):
        pass

    def remove(self, task):
        pass

    def run(self, task):
        pass

    def find(self, name):
        return self.tasks[name]

