from vake import task

@task()
def t1(t):
    print(t)

@task(['t1'])
def t2(t):
    print(t)
