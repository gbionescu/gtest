import time
import gtest.hook as hook


@hook.test(max_concurrency=2)
def conc1():
    i = 0
    while i < 3:
        print("%s %d" % (conc1.__name__, i))
        i += 1
        time.sleep(1)

@hook.test()
def conc3b():
    i = 0
    while i < 3:
        print("%s %d" % (conc3b.__name__, i))
        i += 1
        time.sleep(1)


@hook.test(max_concurrency=1)
def conc2a():
    i = 0
    while i < 3:
        print("%s %d" % (conc2a.__name__, i))
        i += 1
        time.sleep(1)

@hook.test(max_concurrency=2)
def conc2b():
    i = 0
    while i < 3:
        print("%s %d" % (conc2b.__name__, i))
        i += 1
        time.sleep(1)


@hook.test(max_concurrency=3)
def conc3a():
    i = 0
    while i < 3:
        print("%s %d" % (conc3a.__name__, i))
        i += 1
        time.sleep(1)
