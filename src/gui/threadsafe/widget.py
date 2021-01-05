import tkinter as tk
from time import sleep

from .threadsafevar import ThreadSafeVar


UNALLOWED_NAMES = ["__class__", "__repr__", "__getattribute__", "__index__", "__new__", "__doc__"]


class ThreadSafeWidget(ThreadSafeVar):
    __slots__ = ("widget", "args", "kwargs")
    def __init__(self, widgetclass, master, **kwargs):
        super().__init__()
        self.args = (widgetclass, master)
        self.kwargs = kwargs

    def create(self): # Do not call
        super().add_op(self._create, *self.args, **self.kwargs)
        self.wait_created()

    def _create(self, widgetclass, master, **kwargs): # Do not call
        super().set_var(widgetclass(master, **kwargs))