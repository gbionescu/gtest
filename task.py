import asyncio
from multiprocessing import Process

object_needs = {}
object_provide = {}
test_object = []


def add_obj_needing(obj, need):
    if need not in object_needs:
        object_needs[need] = [obj]
    else:
        object_needs[need].append(obj)


def add_obj_providing(obj, provide):
    if provide not in object_needs:
        object_provide[provide] = [obj]
    else:
        object_provide[provide].append(obj)


def add_test_object(new_obj):
    test_object.append(new_obj)


async def run_task(task):
    print("Running " + str(task.func))
    p = Process(target=task.func)
    p.start()
    p.join()


async def get_runnable_task():
    while True:
        for obj in test_object:
            if obj.has_needs_satisfied():
                test_object.remove(obj)
                await run_task(obj)
        await asyncio.sleep(0.1)


def run_tasks():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_runnable_task())
