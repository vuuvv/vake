import unittest

from vake.decorators import task

@task()
def t1(task):
    print(task)

@task(['t1'])
def t2(task):
    print(task)

t2()
