import os
import time
import unittest
import tempfile

from vake.task import Task, FileTask, empty

class TestTask(unittest.TestCase):
    def test_create(self):
        t = Task("t")
        self.assertEquals("t", t.name)
        self.assertEquals([], t.depends)
        self.assertEquals(empty, t.action)
        self.assertTrue(t.needed())

    def test_repr(self):
        t1 = Task("t1")
        t2 = Task("t2")
        t = Task("t", [t1, t2])
        self.assertEquals('<Task t => [t1,t2]>', str(t))

    def test_call(self):
        self.flag = True
        def func(task):
            self.flag = False

        t1 = Task("t1", action=func)
        self.assertEquals(True, self.flag)
        t1()
        self.assertEquals(False, self.flag)

class TestFileTask(unittest.TestCase):
    def setUp(self):
        self.fd1, self.file1 = tempfile.mkstemp()
        time.sleep(0.01)
        self.fd2, self.file2 = tempfile.mkstemp()
        time.sleep(0.01)
        self.fd3, self.file3 = tempfile.mkstemp()
        time.sleep(0.01)
        self.fd4, self.file4 = tempfile.mkstemp()
        os.close(self.fd1)
        os.close(self.fd2)
        os.close(self.fd3)
        os.close(self.fd4)

    def tearDown(self):
        os.remove(self.file1)
        os.remove(self.file2)
        os.remove(self.file3)
        os.remove(self.file4)

    def test_file_out_of_date(self):
        ft1 = FileTask(self.file1)
        ft2 = FileTask(self.file2)
        ft4 = FileTask(self.file4)
        ft3 = FileTask(self.file3, [ft1, ft2, ft4])
        self.assertTrue(ft3.needed())

    def test_file_not_out_of_date(self):
        ft1 = FileTask(self.file1)
        ft2 = FileTask(self.file2)
        ft3 = FileTask(self.file3)
        ft4 = FileTask(self.file4, [ft1, ft2, ft3])
        self.assertFalse(ft4.needed())

    def test_file_not_exist(self):
        f1 = FileTask('file:file_not.exist')
        self.assertTrue(f1.needed())


