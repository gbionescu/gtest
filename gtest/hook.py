import inspect
import enum
import gtest.log as log
import os

from gtest.task import TaskDep
from multiprocessing import Process

log = log.log("hook.log")


@enum.unique
class GTestType(enum.Enum):
    TEST = 1


class GTestObject():
    def __init__(self, func, objtype, kwargs, path):
        self._func = func
        self._path = path.replace(os.getcwd() + "/", "")

        log.debug("Adding func %s" % str(func))

        self._needs = kwargs.get("needs", None)
        self._provides = kwargs.get("provides", None)
        self._max_concurrency = kwargs.get("max_concurrency", None)

        if self._needs:
            if type(self._needs) == list:
                for need in self._needs:
                    TaskDep.add_obj_needing(self, need)
            else:
                TaskDep.add_obj_needing(self, self._needs)
                self._needs = [self._needs]

        if self._provides:
            if type(self._provides) == list:
                for prov in self._provides:
                    TaskDep.add_obj_providing(self, prov)
            else:
                TaskDep.add_obj_providing(self, self._provides)
                self._provides = [self._provides]

        self.proc = None

    def __repr__(self):
        return "%s/%s" % (self._path, self.func.__name__)

    def has_needs_satisfied(self):
        if self._needs:
            return len(self._needs) == 0
        return True

    @property
    def func(self):
        return self._func

    @property
    def max_concurrency(self):
        return self._max_concurrency

    def start_process(self):
        p = Process(target=self.func)
        p.start()

        self.proc = p

    def get_process(self):
        return self.proc

    def is_proc_alive(self):
        if self.proc:
            return self.proc.is_alive()

        return None

    def mark_dependency_solved(self, obj):
        self._needs.remove(obj)

    @property
    def provides(self):
        if self._provides:
            return self._provides
        return []


def test(*args, **kwargs):
    def _object_hook(func):
        TaskDep.add_test_object(
            GTestObject(
                func,
                GTestType.TEST,
                kwargs,
                inspect.stack()[2][1]))
        return func

    if len(args) == 1 and callable(args[0]):
        TaskDep.add_test_object(
            GTestObject(
                args[0],
                GTestType.TEST,
                None,
                inspect.stack()[1][1]))
        return args[0]
    else:
        return lambda func: _object_hook(func)
