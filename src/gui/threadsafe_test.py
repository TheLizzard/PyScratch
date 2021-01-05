from threadsafe.tk import ThreadSafeTk
from threadsafe.widget import ThreadSafeWidget
import tkinter as tk

root = ThreadSafeTk()
root.wait_created()
root.call_method("resizable", False, False)

label = ThreadSafeWidget(tk.Label, root.root, text="https://stackoverflow.com/q/65569984/11106801")
root.add_widget(label)
label.call_method("grid", row=1, column=1, sticky="news")

button = ThreadSafeWidget(tk.Button, root.root, text="Press me 100 times for tkinter to crash", command=root.get_method("mainloop"))
root.add_widget(button)
button.call_method("grid", row=2, column=1, sticky="news")

text = ThreadSafeWidget(tk.Entry, root.root, disabledforeground="black")
root.add_widget(text)
text.call_method("grid", row=3, column=1, sticky="news")
text.call_method("insert", 0, "This is just to test `tk.Entry` (not part of the bug).")
text.call_method("config", state="disabled")

root.take_this_thread()