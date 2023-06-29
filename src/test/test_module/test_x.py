import inspect
import sys

import test_a
import two

def hello():
    print("test_xxxxxxx")
    frameinfo = inspect.stack()[1]
    mod = inspect.getmodule(frameinfo).__name__
    print(mod)
    print("test_xxxxxxx")

def load():
    test_a.load()
    two.load()
    hello()
    print(sys.modules)

load()


