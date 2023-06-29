from inspect import getframeinfo, stack
import os,sys


def asd():
    print(sys.modules)
    print(sys.modules["test_other"])
    print(sys.modules["test_b"])

def get_parent_name():
    print('获取父模块的名称')
    print(os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0])

def give_parent_name():
    return os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0]

