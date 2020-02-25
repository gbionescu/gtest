import task
import hook
import time


@hook.test(provides="a")
def aa():
    print("aa1")
    time.sleep(1)
    print("aa2")


@hook.test(provides="b")
def bb():
    time.sleep(0.1)
    print("bb")


@hook.test(single_exec=True)
def cc():
    time.sleep(1)
    print("cc")


@hook.test(needs=["a", "b"], provides="c")
def asd1():
    print("asd1")


@hook.test(needs=["c"], provides="d")
def asd2():
    print("asd2")


task.run_tasks()
