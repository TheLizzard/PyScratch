from tkinter import Tk as _Tk
from functools import partial
from threading import Thread, current_thread
from time import sleep

from . import tkobj
from .widget import Widget


OTHERDEF_METHODS = set(("bind", "bind_all", "destroy", "quit"))

UNIMPLEM_METHODS = set(("bindtags", "bind_class", "setvar", "mainloop", "unbind_class", "update", "update_idletasks", "wait_variable", "waitvar"))


class Tk(Widget):
    # You can only use these vars:
    __slots__ = ("closed", "widgets")
    # Do not touch these:
    __slots__ += ("tk", "_last_child_ids", "_w", "children")

    def __init__(self, **kwargs):
        self.tk_dead = False
        self.closed = False
        self.widgets = []
        super().__init__()
        t = Thread(target=self.create_obj, kwargs=kwargs, daemon=True)
        t.start()
        super().wait_created()

    def create_obj(self, delay=100, **kwargs):
        """
        Creates the actual tkinter window.
        This thread must not die.
        """

        # Save the thread id for later use:
        tkobj.TKINTER_THREAD = current_thread().ident

        root = _Tk(**kwargs)
        super().set_var(root)

        # Make tkinter happy and think that this
        # is the real tkinter `Tk`
        self.tk = root.tk
        self.master = root.master
        self._last_child_ids = root._last_child_ids
        self._w = root._w
        self.children = root.children

        super().copy(exclude=UNIMPLEM_METHODS, without_get=set(("after", )))

        root.protocol("WM_DELETE_WINDOW", self.destroy)

        self.var.after(0, self._mainloop, delay)
        self.var.update()

    def _mainloop(self, delay=100):
        while not self.closed:
            # Flush all of the operations from the queue
            super().flush_ops(self.var.update_idletasks)
            for widget in self.widgets:
                if len(widget.ops) > 0:
                    widget.flush_ops(self.var.update_idletasks)
            self.var.update()
            sleep(delay/1000) # Convert to seconds
        while not self.tk_dead:
            super().flush_ops(self.var.update_idletasks)
        super().destroy()

    # def _mainloop(self, delay=100):
    #     if not self.closed:
    #         self.var.after(100, self._mainloop, delay)
    #         # Flush all of the operations from the queue
    #         super().flush_ops(self.var.update_idletasks)
    #         for widget in self.widgets:
    #             if len(widget.ops) > 0:
    #                 widget.flush_ops(self.var.update_idletasks)
    #     else:
    #         while not self.tk_dead:
    #             super().flush_ops(self.var.update_idletasks)
    #         super().destroy()

    def add_widget(self, widget):
        self.widgets.append(widget)

    def kill_tk(self):
        self.tk_dead = True

    # Normal tkinter `Tk` methods that are safe to call.
    def bind(self, sequence=None, func=None, add=None):
        return super.bind(sequence=sequence, func=func, add=add, get=True)
    
    def bind_all(self, sequence=None, func=None, add=None):
        return super.bind_all(sequence=sequence, func=func, add=add, get=True)

    def quit(self):
        self.closed = True
        super().call_method_name("quit")

    def destroy(self):
        self.closed = True
        super().call_method_name("quit", get=False)
        super().call_method_name("destroy", get=False)
        super().call_method(self.kill_tk, get=True)