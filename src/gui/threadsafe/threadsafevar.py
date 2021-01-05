from time import sleep

#from .varplaceholder import VarPlaceHolder
from .operations import Operations


class ThreadSafeVar:
    __slots = ("ops", "variable")
    def __init__(self, variable=None):
        self.var = variable
        self.ops = Operations()

    def wait_created(self, timestep=0.2):
        while self.var is None:
            sleep(timestep)

    def call_method(self, method_name, *args, **kwargs):
        return self.ops.add(self._call_method, method_name, *args, **kwargs)

    def get_method(self, method_name):
        return getattr(self.var, method_name)

    def _call_method(self, method_name, *args, **kwargs):
        return getattr(self.var, method_name)(*args, **kwargs)

    def flush_ops(self):
        self.ops.flush_ops()

    def set_var(self, var):
        self.var = var

    def add_op(self, *args, **kwargs):
        self.ops.add(*args, **kwargs)