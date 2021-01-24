from functools import partial
import tkinter as _tk

from .widget import Widget


class Button(Widget):
    UNIMPLEM_METHODS = set(tuple())

    def __init__(self, master, command=None, **kwargs):
        if command is not None:
            command = partial(super().call_function_wrapper, command)
        super().__init__()
        master.add_widget(self)
        super().call_method(self.create_obj, master, command=command, **kwargs)
        super().wait_created()

    def create_obj(self, master, **kwargs):
        var = _tk.Button(master, **kwargs)
        super().set_var(var)
        super().copy(exclude=self.UNIMPLEM_METHODS)
        self.old_config = self.config
        self.config = self.new_config

    def new_config(self, **kwargs):
        if "command" in kwargs:
            command = kwargs["command"]
            kwargs.update({"command", partial(super().call_function_wrapper, command)})
        self.old_config(**kwargs)


class Label(Widget):
    UNIMPLEM_METHODS = set(tuple())

    def __init__(self, master, **kwargs):
        super().__init__()
        master.add_widget(self)
        super().call_method(self.create_obj, master, **kwargs)
        super().wait_created()

    def create_obj(self, master, **kwargs):
        var = _tk.Label(master, **kwargs)
        super().set_var(var)
        super().copy(exclude=self.UNIMPLEM_METHODS)


class Entry(Widget):
    UNIMPLEM_METHODS = set(tuple())

    def __init__(self, master, **kwargs):
        super().__init__()
        master.add_widget(self)
        super().call_method(self.create_obj, master, **kwargs)
        super().wait_created()

    def create_obj(self, master, **kwargs):
        var = _tk.Entry(master, **kwargs)
        super().set_var(var)
        super().copy(exclude=self.UNIMPLEM_METHODS)


class Canvas(Widget):
    UNIMPLEM_METHODS = set(tuple())
    # WITHOUT = set(("create_arc", "create_bitmap", "create_image",
    #                "create_line", "create_oval", "create_polygon",
    #                "create_rectangle", "create_text", "create_window"))

    def __init__(self, master, **kwargs):
        super().__init__()
        master.add_widget(self)
        super().call_method(self.create_obj, master, **kwargs)
        super().wait_created()

    def create_obj(self, master, **kwargs):
        var = _tk.Canvas(master, **kwargs)
        super().set_var(var)
        super().copy(exclude=self.UNIMPLEM_METHODS)