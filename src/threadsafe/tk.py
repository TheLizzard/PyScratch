from threading import Thread, current_thread
from functools import partial
from datetime import datetime
from time import sleep
import tkinter as _tk
from os import system

from .widget import Widget
from .widgets import Label, Frame
from . import tkobj


OTHERDEF_METHODS = set(("bind", "bind_all", "destroy", "quit", "update"))

UNIMPLEM_METHODS = set(("bindtags", "bind_class", "setvar", "mainloop", "unbind_class", "update", "update_idletasks", "wait_variable", "waitvar"))


class Tk(Widget):
    # You can only use these vars:
    __slots__ = ("closed", "widgets", "autoupdate", "updated")
    # Do not touch these:
    __slots__ += ("tk", "_last_child_ids", "_w", "children")

    def __init__(self, autoupdate=True, debug=False, max_fps=30, **kwargs):
        self.update_delay = 1/max_fps
        self.autoupdate = autoupdate
        self.tk_dead = False
        self.updated = True
        self.closed = False
        self.debug = debug
        if self.debug:
            self.loading_start = datetime.now()
            self.delta_time_backlog = []
        self.widgets = []
        super().__init__()
        t = Thread(target=self.create_obj, kwargs=kwargs, daemon=True)
        t.start()
        super().wait_created()

    def create_obj(self, **kwargs):
        """
        Creates the actual tkinter window.
        This thread must not die.
        """

        # Save the thread id for later use:
        tkobj.TKINTER_THREAD = current_thread().ident

        root = _tk.Tk(**kwargs)
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

        self.var.after(0, self._mainloop)
        self.var.update()

    def _mainloop(self):
        self.last_updated = datetime.now()
        if self.debug:
            debug_frame = _tk.Frame(self.var)
            debug_frame.grid(row=0, column=1)

            self.loading_time = datetime.now() - self.loading_start
            time_delta = self.loading_time.seconds + self.loading_time.microseconds/(10**6)
            label_loading_time = _tk.Label(debug_frame, text="Loading time: %s" % str(time_delta))
            label_loading_time.grid(row=1, column=1)

            label_fps = _tk.Label(debug_frame, text="FPS: Collecting data")
            label_fps.grid(row=1, column=2)

        while not self.closed:
            start_frame_time = datetime.now()
            # Get the FPS
            # Get the timedelta and reset self.last_updated
            time_delta = datetime.now() - self.last_updated
            self.last_updated = datetime.now()
            # Adding 1 so that it never raises ZeroDivisionError
            seconds_delta = time_delta.seconds + (time_delta.microseconds+1)/(10**6)

            self.delta_time_backlog.append(seconds_delta)
            # print(self.fps_backlog)
            self.delta_time_backlog = self.delta_time_backlog[-30:]
            fps_avg = len(self.delta_time_backlog) / sum(self.delta_time_backlog)

            if self.debug:
                # Show the fps onthe screen:
                label_fps.config(text="FPS: %s" % str(int(fps_avg+0.5)))

            # Flush all of the operations from the queue
            super().flush_ops(self.var.update_idletasks)
            for widget in self.widgets:
                if len(widget.ops) > 0:
                    widget.flush_ops(self.var.update_idletasks)
            if self.autoupdate or not self.updated:
                self.var.update()
            else:
                self.var.update_idletasks()
            self.updated = True

            delta_time = datetime.now() - start_frame_time
            # The last term is a correct value as `time.sleep` takes (on average) 0.032133814 sec longer
            # but for some reason that doesn't work so I am sticking with 0.004
            time_to_sleep = self.update_delay - delta_time.seconds - delta_time.microseconds/10**6 - 0.004
            if time_to_sleep > 0:
                sleep(time_to_sleep)
        while not self.tk_dead:
            super().flush_ops(self.var.update_idletasks)
        super().destroy()

    def add_widget(self, widget):
        self.widgets.append(widget)

    def kill_tk(self):
        self.tk_dead = True

    def take_this_thread(self, timestep=300):
        while not self.closed:
            sleep(timestep/1000)

    def take_this_thread_debug(self):
        while not self.closed:
            _in = input("System: ")
            system(_in)

    def update(self, timestep=100):
        self.updated = False
        while not self.updated:
            sleep(timestep/1000)

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