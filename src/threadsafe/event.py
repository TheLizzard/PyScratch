from tkinter import Event as _Event


class Event:
    def __init__(self, tcl_event: _Event):
        self.tcl_event = tcl_event

    def __repr__(self):
        return "Event(tcl_event=%s)" % repr(self.tcl_event)

    def __str__(self):
        return repr(self)