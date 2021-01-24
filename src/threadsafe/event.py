from tkinter import Event as _Event


class Event:
    def __init__(self, event: _Event):
        self.event = event