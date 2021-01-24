from functools import partial
from threading import Lock
from time import sleep


class NotDoneYet:
    pass


class Operation:
    __slots__ = ("target", "args", "kwargs", "result")
    def __init__(self, target, *args, **kwargs):
        self.target = partial(target, *args, **kwargs)
        self.result = NotDoneYet()

    def __call__(self, callback_when_in_loop=None):
        self.result = self.target()

    def __repr__(self):
        output = "Operation(%s"
        output %= str(self.target.func)

        args = ", ".join(map(str, self.target.args))
        if args != "":
            output += ", %s"%args

        kwargs = str(self.target.keywords)[1:-1]
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