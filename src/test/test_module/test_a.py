from importlib import import_module
from inspect import stack

def hello():
    frame, filename, line_number, function_name, lines, index = stack()[2]
    print(frame, filename, line_number, function_name, lines, index)


def a():
    test_b = import_module("test_b")
    test_b.b()

def load():
    a()
    hello()

