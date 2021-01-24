import inspect
import sys


global DEBUG_LEVEL
DEBUG_LEVEL = "mine" # Can also be: "mine"
# all is for all functions called.
# mine if just for the functions that the user has defined (the ones not in "C:\\Program Files\\Python37")


class StackDebug:
    def __init__(self, file="debug.txt", debug_lebel="mine"):
        global DEBUG_LEVEL
        DEBUG_LEVEL = debug_lebel
        self.file = file
        self.data = []
    
    def write(self, string):
        self.data.append(string)

    def __enter__(self):
        global DEBUG_FILE
        DEBUG_FILE = self
        self.write("="*50+" Starting debug "+"="*50)
        sys.setprofile(stack_debugger)

    def __exit__(self, *args):
        sys.setprofile(None)
        self.write("="*50+" End debug "+"="*50)
        with open(self.file, "w") as file:
            file.write(self.clean_up_data(self.data))

    def clean_up_data(self, data):
        longest = []
        output = ""

        for line in data:
            parts = line.split("\t")
            if len(parts) == 1:
                continue
            for idx in range(len(parts)):
                if len(longest) == idx:
                    longest.append(len(parts[idx]))
                else:
                    longest[idx] = max(longest[idx], len(parts[idx]))

        longest = [i+3 for i in longest]
        for line in data:
            parts = line.split("\t")
            if len(parts) == 1:
                output += line+"\n"
                continue
            for idx in range(len(parts)-1):
                part = parts[idx]
                length = len(part)
                output += part + " "*(longest[idx]-length)
            output += parts[-1]
            output += "\n"

        return output


def get_class_from_frame(frame):
    args, _, _, value_dict = inspect.getargvalues(frame)
    # we check the first parameter for the frame function is
    # named "self"
    if len(args) and args[0] == "self":
        # in that case, "self" will be referenced in value_dict
        instance = value_dict.get("self", None)
        if instance:
            # return its class
            return getattr(instance, "__class__", None)
    # return None otherwise
    return None


def stack_debugger(frame, event, args, indent=[0]):
    global DEBUG_LEVEL

    filename = str(frame.f_code.co_filename)
    _class = get_class_from_frame(frame)
    method_name = str(frame.f_code.co_name)
    if _class is not None:
        method_name = _class.__name__+"."+method_name

    if DEBUG_LEVEL == "mine":
        a = "C:\\Program Files\\Python37" in filename
        b = filename.startswith("<frozen importlib.")
        c = ("<" == filename[0]) and (">" == filename[-1])
        if a or b or c:
            return None

    if event == "call":
        indent[0] += 2
        text = "-"*indent[0] + ">"
        text += "\t%s()\t%s" % (method_name, filename)
        DEBUG_FILE.write(text)

    elif event == "return":
        if args is None:
            args = "None"
        elif isinstance(args, tuple):
            args = ", ".join(map(str, args))
        else:
            args = str(args)

        text = "<" + "-" * indent[0]
        text += "\t%s => %s\t%s" % (method_name, args, filename)
        indent[0] -= 2
        DEBUG_FILE.write(text)


def add_to_debug(text):
    global DEBUG_LEVEL
    if DEBUG_FILE is not None:
        DEBUG_FILE.write(text)


if __name__ == "__main__":
    def f(var):
        return var*3

    with StackDebug():
        f("a")