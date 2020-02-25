import inspect
import enum
import task

@enum.unique
class GTestType(enum.Enum):
    TEST = 1


class GTestObject():
    def __init__(self, func, objtype, kwargs, path):
        self._func = func
        self._path = path

        self._needs = kwargs.get("needs", None)
        self._provides = kwargs.get("provides", None)
        self._single_exec = kwargs.get("single_exec", False)

        if self._needs:
            if type(self._needs) == list:
                for need in self._needs:
                    task.add_obj_needing(self, need)
            else:
                task.add_obj_needing(self, self._needs)

        if self._provides:
            if type(self._provides) == list:
                for prov in self._provides:
                    task.add_obj_providing(self, prov)
            else:
                task.add_obj_providing(self, self._provides)

    def has_needs_satisfied(self):
        if self._needs:
            return len(self._needs) == 0
        return True

    @property
    def func(self):
        return self._func


def test(*args, **kwargs):
    def _object_hook(func):
        task.add_test_object(
            GTestObject(
                func,
                GTestType.TEST,
                kwargs,
                inspect.stack()[2][1]))
        return func

    if len(args) == 1 and callable(args[0]):
        task.add_test_object(
            GTestObject(
                args[0],
                GTestType.TEST,
                None,
                inspect.stack()[1][1]))
        return args[0]
    else:
        return lambda func: _object_hook(func)
