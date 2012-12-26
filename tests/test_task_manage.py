# -*- coding: utf-8 -*-
import unittest

from vake.task import Task
from vake.manage import TaskManage, DuplicatedTaskName, TaskNotFound

class TestTaskManage(unittest.TestCase):
    def setUp(self):
        self.manage = TaskManage()

    def test_add_duplication(self):
        with self.assertRaises(DuplicatedTaskName) as context:
            name = 'duplicate name'
            self.manage.add(Task(name))
            self.manage.add(Task(name))

    def test_remove(self):
        name = 'I will be remove'
        self.manage.add(Task(name))
        self.manage.remove(name)
        with self.assertRaises(TaskNotFound):
            self.manage.find(name)

    def test_invoke(self):
        runlist = []
        t1 = Task('t1', action=lambda t: runlist.append(t.name))
        t2 = Task('t2', action=lambda t: runlist.append(t.name))
        self.manage.add(t1)
        self.manage.add(t2)
        self.manage.add(Task('t3', depends=[t1, t2],
                        action = lambda t: runlist.append(t.name)))
        self.manage.invoke('t3')
        self.assertEqual(runlist, ['t1', 't2', 't3'])

    def test_invoke_with_circular_dependencies(self):
        runlist = []
        t1 = Task('t1')
        t2 = Task('t2', depends=[t1])
        t1.depends = [t2]
        self.manage.add(t1)
        self.manage.add(t2)

        with self.assertRaises(RuntimeError):
            self.manage.invoke('t1')

    def test_no_double_invoke(self):
        runlist = []
        t1 = Task('t1', action=lambda t: runlist.append(t.name))
        t2 = Task('t2', depends=[t1], action=lambda t: runlist.append(t.name))
        t3 = Task('t3', depends=[t2, t1], action=lambda t: runlist.append(t.name))
        self.manage.add(t1)
        self.manage.add(t2)
        self.manage.add(t3)
        self.manage.invoke('t3')
        self.assertEqual(['t1', 't2', 't3'], runlist)
