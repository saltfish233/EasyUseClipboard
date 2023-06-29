import sys
from importlib import import_module
from inspect import getframeinfo, stack
import os,sys




def b():
    print("two b----")
    test_c = import_module("test_c")
    test_c.c()
    hello()
    print("two b----")
# test_other.asd()
# print(sys.modules["test_b"])
# print(__file__)

def hello():
    frame, filename, line_number, function_name, lines, index = stack()[2]
    print(frame, filename, line_number, function_name, lines, index)