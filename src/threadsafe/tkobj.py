global TKINTER_THREAD
TKINTER_THREAD = None

from functools import partial
from threading import Lock, current_thread
from time import sleep
import traceback

from .stackdebugger import add_to_debug
from .operation import Operation
from .event import Event


class TkObj:
    __slots = ("ops", "var", "lock", "created")

    def __init__(self):
        self.created = False
        self.lock = Lock()
        self.var = None
        self.ops = []

    def set_var(self, var):
        """
        Setts the variable to be held by this object.
        """
        self.var = var

    def call_function_wrapper(self, func):
        try:
            result = func()
        except Exception as error:
            result = error
            text = "    "+"="*50+" Error Start "+"="*50+"\n"
            text += "    str(error) = \"%s\"\n    "%str(error)
            text += traceback.format_exc().replace("\n", "\n    ")
            text += "="*50+" Error End "+"="*50+"\n"
            add_to_debug(text)
            print("\n"+text, end="")
        return result

    def _bind_call_wrapper(self, func, event):
        func_plus_event = partial(func, Event(event))
        return self.call_function_wrapper(func_plus_event)

    def wait_created(self, timestep=0.2, callback_when_in_loop=None):
        """
        Waits until the object is visible on the screen.
        """
        if callback_when_in_loop is None:
            callback_when_in_loop = lambda: None
        while not self.created:
            callback_when_in_loop()
            sleep(timestep)

    def call_method_name(self, method_name, *args, get=False, **kwargs):
        """
        Gets the method from the method name and adds the
        command a queue of operations to be completed next
        time it recieves flush_ops. Returns an `Operation`
        object.
        """
        global TKINTER_THREAD
        if current_thread().ident == TKINTER_THREAD:
            return getattr(self.var, method_name)(*args, **kwargs)
        return self.call_method(getattr(self.var, method_name), *args, get=get, **kwargs)

    def call_method(self, method, *args, get=False, **kwargs):
        """
        Adds the command a queue of operations to be
        completed next time it recieves flush_ops. Returns
        an `Operation` object.
        """
        assert callable(method), "The method must be callable. Use `call_method_name` instead."
        op = Operation(method, *args, **kwargs)
        with self.lock:
            self.ops.append(op)
        if get:
            return op.get()
        return op

    def flush_ops(self, callback_when_in_loop=None):
        """
        Flushes all of the operations. Only to be called in
        the correct thread.
        """
        if callback_when_in_loop is None:
            callback_when_in_loop = lambda: None
        with self.lock:
            try:
                for operation in self.ops:
                    operation(callback_when_in_loop=callback_when_in_loop)
            except Exception as error:
                print("Error")
                self.ops.clear()
                raise error
            self.ops.clear()

    def clear_ops(self):
        """
        Cears all `operation` objects from the list (`ops`)
        """
        with self.lock:
            self.ops.clear()