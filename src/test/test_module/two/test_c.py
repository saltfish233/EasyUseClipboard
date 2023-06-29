from inspect import getframeinfo, stack, currentframe
import os,sys

def c():
    hello()

def get_parent_name():
    print('获取父模块的名称')
    print(os.path.splitext(os.path.basename(getframeinfo(stack()[-1][0]).filename))[0])

def hello():
    frame, filename, line_number, function_name, lines, index = stack()[2]
    print(frame, filename, line_number, function_name, lines, index)