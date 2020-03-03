import time
import gtest.hook as hook


@hook.test(provides="b")
def bb():
    i = 0
    while i < 3:
        print("bb %d" % i)
        i += 1
        time.sleep(1)


@hook.test(provides="a", max_concurrency=2)
def aa():
    i = 0
    while i < 3:
        print("aa %d" % i)
        i += 1
        time.sleep(1)


@hook.test(max_concurrency=2)
def aaa():
    i = 0
    while i < 3:
        print("aaa %d" % i)
        i += 1
        time.sleep(1)

@hook.test(max_concurrency=2)
def aaaa():
    i = 0
    while i < 3:
        print("aaaa %d" % i)
        i += 1
        time.sleep(1)

@hook.test()
def cc():
    i = 0
    while i < 3:
        print("cc %d" % i)
        i += 1
        time.sleep(1)


@hook.test(needs="a", max_concurrency=1)
def bbb():
    i = 0
    while i < 3:
        print("bbb %d" % i)
        i += 1
        time.sleep(1)


@hook.test(needs="a")
def asd1():
    print("xxx1")

@hook.test(needs=["a", "b"], provides="c")
def asd1():
    print("asd1")


@hook.test(needs=["a"], provides="d")
def asd2():
    print("asd2")
