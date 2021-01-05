from threading import Lock
from time import sleep

from .partial import partial


class NotDoneYet:
    pass


class Operation:
    __slots__ = ("target", "args", "kwargs", "result")
    def __init__(self, target, *args, **kwargs):
        self.target = partial(target, *args, **kwargs)
        self.result = NotDoneYet()

    def __repr__(self):
        output = "Operation(%s"
        output %= str(self.target.function)

        args = ", ".join(map(str, self.target.args))
        if args != "":
            output += ", %s"%args

        kwargs = str(self.target.kwargs)[1:-1]
        if kwargs != "":
            output += ", %s"%kwargs

        return output+")"

    def wait(self, timestep=0.2, callback=None):
        while isinstance(self.result, NotDoneYet):
            if callback is not None:
                callback()
            sleep(timestep)

    def get(self):
        self.wait()
        return self.result

    def exec(self):
        try:
            result = self.target()
        except Exception as error:
            result = error
        self.result = result


"""
Stores a list of `Operation` objects.
Debug:
    "ops"     to see the addition and execution of each of the `Operation` objects
"""


class Operations:
    __slots__ = ("lock", "ops", "debug")
    def __init__(self, debug=""):
        self.lock = Lock()
        self.ops = []
        self.debug = debug

    def add(self, target, *args, **kwargs):
        op = Operation(target, *args, **kwargs)
        if "ops" in self.debug:
            print("[add]    "+repr(op))
        with self.lock:
            self.ops.append(op)
        return op

    def exec(self):
        with self.lock:
            for op in self.ops:
                if "ops" in self.debug:
                    print("[exec]   "+repr(op))
                op.exec()
            self.ops = []

    def flush_ops(self):
        self.exec()

    def flush(self):
        self.exec()

    def delete_all(self):
        with self.lock:
            self.ops = []