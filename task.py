import asyncio
import log
import sys

log = log.log("task.log")

class TaskDep():
    object_needs = {}
    object_provide = {}
    test_object = []

    @staticmethod
    def add_obj_needing(obj, need):
        log.debug("[%s] Needs %s" % (str(obj), need))
        if need not in TaskDep.object_needs:
            TaskDep.object_needs[need] = [obj]
        else:
            TaskDep.object_needs[need].append(obj)

    @staticmethod
    def add_obj_providing(obj, provide):
        log.debug("[%s] Provides %s" % (str(obj), provide))
        if provide in TaskDep.object_provide:
            raise ValueError(
                "There already is an object providing %s" % (str(obj)))

        TaskDep.object_provide[provide] = obj

    @staticmethod
    def check_dangling_needs():
        """
        Check that all tasks have needs covered by a provider
        """

        for need in TaskDep.object_needs:
            if need not in TaskDep.object_provide:
                raise ValueError("%s has no provider" % str(need))

    @staticmethod
    def mark_dependency_solved(obj):
        if obj not in TaskDep.object_needs:
            print("No task needs %s" % str(obj))
            return

        for target in TaskDep.object_needs[obj]:
            target.mark_dependency_solved(obj)

    @staticmethod
    def add_test_object(new_obj):
        TaskDep.test_object.append(new_obj)

    @staticmethod
    def rem_test_object(new_obj):
        TaskDep.test_object.remove(new_obj)

    @staticmethod
    def to_test():
        return list(TaskDep.test_object)

    @staticmethod
    def finished():
        return len(TaskDep.test_object) == 0


class TaskRunner():
    tasks = []
    pool_size = sys.maxsize
    finished = False

    @staticmethod
    def set_pool_size(new_size, force=False):
        if not new_size:
            return

        if not force:
            if TaskRunner.pool_size > new_size:
                log.debug("New pool size is %d" % new_size)
                TaskRunner.pool_size = new_size
        else:
            log.debug("New pool size is %d (forced)" % new_size)
            TaskRunner.pool_size = new_size

    @staticmethod
    def can_run_in_pool(req_concur):
        # log.debug(
        #     "Check run req %s avail %s" % (
        #         req_concur if type(req_concur) == int else 0,
        #         TaskRunner.pool_size if TaskRunner.pool_size != sys.maxsize else "MAX"))

        if req_concur and req_concur < len(TaskRunner.tasks):
            return False

        # Check if there is room in the pool
        if TaskRunner.pool_size - len(TaskRunner.tasks) - 1 <= 0:
            return False

        return True

    @staticmethod
    async def monitor_tasks():
        while True:
            for task in list(TaskRunner.tasks):
                if task.is_proc_alive():
                    continue

                for prov in task.provides:
                    TaskDep.mark_dependency_solved(prov)

                log.debug("%s exited" % str(task))
                TaskRunner.tasks.remove(task)

            min_concurrency = sys.maxsize
            for task in list(TaskRunner.tasks):
                if task.max_concurrency:
                    min_concurrency = \
                        min(min_concurrency, task.max_concurrency)

            if min_concurrency != TaskRunner.pool_size:
                TaskRunner.set_pool_size(min_concurrency, force=True)

            # Exit if there are no other tasks and the queue is empty
            if TaskRunner.finished:
                return

            await asyncio.sleep(0.1)

    @staticmethod
    async def run_task(task):
        log.debug("Starting %s" % str(task))

        TaskRunner.set_pool_size(task.max_concurrency)
        task.start_process()
        TaskRunner.tasks.append(task)

    @staticmethod
    async def get_runnable_task():
        to_run = []
        while not TaskDep.finished() or len(to_run) > 0:
            for obj in TaskDep.to_test():
                # If object has no needs
                if obj.has_needs_satisfied():
                    log.debug("Enqueue %s" % str(obj))

                    TaskDep.rem_test_object(obj)
                    to_run.append(obj)

            for runnable in to_run:
                # Check if max_concurrency condition is achieved
                if TaskRunner.can_run_in_pool(runnable.max_concurrency):
                    to_run.remove(runnable)
                    await TaskRunner.run_task(runnable)

            await asyncio.sleep(1)

        TaskRunner.finished = True


def run_tasks():
    # Make sure that all needs have providers
    TaskDep.check_dangling_needs()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        asyncio.gather(
            TaskRunner.get_runnable_task(),
            TaskRunner.monitor_tasks())
        )
