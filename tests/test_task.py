import unittest

from vake.task import Task, empty

class TestTask(unittest.TestCase):
    def test_create(self):
        t = Task("t")
        self.assertEquals("t", t.name)
        self.assertEquals([], t.depends)
        self.assertEquals(empty, t.action)
        self.assertFalse(t.out_of_date())

    def test_repr(self):
        t1 = Task("t1")
        t2 = Task("t2")
        t = Task("t", [t1, t2])
        self.assertEquals('<Task t => [t1,t2]>', str(t))

    def test_call(self):
        self.flag = True
        def func(name, depends):
            self.flag = False

        t1 = Task("t1", action=func)
        self.assertEquals(True, self.flag)
        t1()
        self.assertEquals(False, self.flag)

