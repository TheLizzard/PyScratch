class TestClass:
    def __init__(self):
        self.value = 5
    
    def __add__(self, other):
        return self.value+other

    def set(self, new_value):
        self.value = new_value


class VarPlaceHolder:
    def __init__(self):
        self.var = None

    def inherit(self, var):
        self.__dict__ = var.__dict__
        self.var = var
        for method_name in dir(var):
            method = getattr(var, method_name)
            if callable(method):
                setattr(self, method_name, method)


if __name__ == "__main__":
    print("Testing program")
    obj = TestClass()
    a = VarPlaceHolder()
    a.inherit(obj)

    assert (a+5) == 10 # Test magic methods (`TestClass.__add__`)
    a.set(10) # Test normal methods (`TestClass.set`)
    assert (a+5) == 15 # Test that the line obove worked
    assert a.__dict__["value"] == 10 # Test that we can access the `__dict__` of the super object
    assert a.value == 10 # Test that we can access the `value` of the super object
    assert getattr(a, "value") == 10 # Test if getattr works
    print("All tests passed")