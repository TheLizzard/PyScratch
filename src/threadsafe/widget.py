from functools import partial

from .tkobj import TkObj


DONT_COPY = set(("__class__", "__weakref__", "bind", "bind_all"))
WITHOUT_GET = set(("config", ))


class Widget(TkObj):
    def __init__(self):
        super().__init__()

    def destroy(self):
        super().call_method(self.destroy_tcl, get=True)

    def destroy_tcl(self):
        """
        Destoys the tk variable and makes sure that we
        don't have a reference to it otherwise we get:
            Tcl_AsyncDelete: async handler deleted by the wrong thread
            https://bugs.python.org/issue39093
        """
        self.var.destroy()
        del self.var

    def bind(self, sequence=None, func=None, add=None):
        func = partial(super()._bind_call_wrapper, func)
        super().call_method_name("bind", sequence=sequence, func=func, add=add, get=True)

    def bind_all(self, sequence=None, func=None, add=None):
        func = partial(super()._bind_call_wrapper, func)
        super().call_method_name("bind_all", sequence=sequence, func=func, add=add, get=True)

    def copy(self, exclude=set(), override=set(), without_get=set()):
        assert self.var is not None, "You haven't set the variable"
        for method_name in dir(self.var):
            if callable(getattr(self.var, method_name)):
                if (method_name not in exclude) and (method_name not in DONT_COPY):
                    if (method_name not in dir(self)) or (method_name in override):
                        get = True
                        if (method_name in without_get) or (method_name in WITHOUT_GET):
                            get = False
                        method = partial(super().call_method_name, method_name, get=get)
                        setattr(self, method_name, method)
        self.created = True