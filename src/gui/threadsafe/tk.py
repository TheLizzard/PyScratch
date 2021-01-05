from threading import Thread, Lock
from time import sleep
import tkinter as tk
import os

from .threadsafevar import ThreadSafeVar


UNALLOWED_NAMES = ["__class__", "__weakref__", "__repr__", "__getattribute__", "__index__", "__new__", "__doc__"]


class ThreadSafeTk(ThreadSafeVar):
    """
    A thread safe tkinter.Tk class
    Methods
        Note: if the method says: "Call only from thread 2." do not call it
            it will crash tkinter. Thread 2 is internally created and is only
            to be called from internal tkinter methods.
        
        add_widget(widget: ThreadSafeWidget)
            adds the widget to the list of widgets to constantly update

        call_method(methodname: str)
            Calls the internal method and returns the result

        All other tkinter.Tk methods
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.widgets = []
        self.closed = False
        t = Thread(target=self.create, kwargs=kwargs, daemon=True)
        t.start()

    def quit(self):
        super().add_op(self.var.quit)
        self.closed = True

    def destroy(self):
        super().add_op(self.var.quit)
        super().add_op(self.var.destroy)
        self.closed = True

    def create(self, **kwargs): # Do not call
        self.root = tk.Tk(**kwargs)
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        super().set_var(self.root)
        self.mainloop()
        self.root.mainloop()

    def mainloop(self): # Do not call
        if not self.closed:
            self.var.after(100, self.mainloop)
            for widget in self.widgets:
                widget.flush_ops()
            super().flush_ops()
            self.var.update()
        else:
            # This should only be called once:
            super().flush_ops()
            self.var.after(100, self.mainloop)

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.create()

    def take_this_thread(self):
        print("This thread is fully controlled by the GUI.\nType exit to close or any other command to execute as a teminal command.")
        while not self.closed:
            _in = input(">>> ")
            if _in.lower().startswith("exit"):
                self.closed = True
            else:
                os.system(_in)