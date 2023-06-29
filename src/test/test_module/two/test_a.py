from importlib import import_module
import inspect

def hello():
    print("test_aaaaa2222")
    frame = inspect.currentframe()
    frame = frame.f_back.f_back

    mod = inspect.getmodule(frame)
    print(mod)
    print("test_aaaaa2222")


def a():
    test_b = import_module("two.test_b")
    test_b.b()

def load():
    a()
    hello()



