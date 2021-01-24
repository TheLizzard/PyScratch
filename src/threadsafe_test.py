"""
Bug: https://bugs.python.org/issue39093
"""


# Uses a bug in the actual tkinter
def real_tcl_asyncdelete_test():
    import tkinter as tk
    import threading
    import time
    
    #create/run_gui()
    root = tk.Tk()
    root.destroy()

    #give to another thread and delete the reference
    def mayfly_func(obj):
        time.sleep(1)

    mayfly = threading.Thread(target=mayfly_func, args=(root,))
    mayfly.start()
    del root

    # Wait until `mayfly_func` as started
    time.sleep(2)

def tcl_asyncdelete_test():
    from threadsafe import Tk, Label, Button
    from time import sleep

    from threading import Thread

    root = Tk()
    root.wait_created()
    root.destroy()
    sleep(2)

def root_tcl_asyncdelete_test():
    import threadsafe as tk
    import threading
    import time

    #create/run_gui()
    root = tk.Tk()
    root.destroy()

    #give to another thread and delete the reference
    def mayfly_func(obj):
        time.sleep(1)

    mayfly = threading.Thread(target=mayfly_func, args=(root,))
    mayfly.start()
    del root

    # Wait until `mayfly_func` as started
    time.sleep(2)

"""
Test if we can create and call root from different threads
"""

def window_test():
    import threadsafe as tk
    import threading
    import time

    def call_resizable(root):
        root.resizable(False, False)

    root = tk.Tk()

    # Call resize from a different thread:
    new_thread = threading.Thread(target=call_resizable, args=(root, ), daemon=True)
    new_thread.start()

    # Make sure that the resize function was called
    time.sleep(2)

    # Destroy the root
    root.destroy()

def widgets_test():
    import threadsafe as tk
    import threading
    import time

    root = tk.Tk()
    root.resizable(False, False)

    label = tk.Label(root, text="This is just to test `tk.Label`.")
    label.grid(row=1, column=1, sticky="news")

    global entry_state
    entry_state = "disabled"
    entry = tk.Entry(root, disabledforeground="black")
    entry.grid(row=3, column=1, sticky="news")
    entry.insert(0, "This is just to test `tk.Entry`.")
    entry.config(state=entry_state)

    def toggle_entry():
        #global entry_state
        if entry_state == "disabled":
            entry_state = "normal"
        else:
            entry_state = "disabled"
        entry.config(state=entry_state)

    def create_button_in_new_thread(root):
        button = tk.Button(root, text="Press me to disable/enable the entry bellow", command=toggle_entry)
        button.grid(row=2, column=1, sticky="news")

    t = threading.Thread(target=create_button_in_new_thread, daemon=True, args=(root, ))
    t.start()

    time.sleep(2)
    root.destroy()
    time.sleep(2)

def after_script_test():
    import threadsafe as tk
    from time import sleep
    import threading

    def loop(root):
        root.after(100, loop, root)

    root = tk.Tk()
    root.resizable(False, False)

    root.after(0, loop, root)

    sleep(2) # Make sure the above runs
    root.destroy()
    sleep(2)


print("Test 1")
root_tcl_asyncdelete_test() # Check if new thinter crashes from old tkinter bug
print("Test 2")
tcl_asyncdelete_test() # Check if the bug persists in the new tkinter
print("Test 3")
widgets_test() # Test if the widgets work
print("Test 4")
after_script_test() # Test if `after` works properly

# from threadsafe import StackDebug

# with StackDebug("debug.txt", "all"):
#     my_code()