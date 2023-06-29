from .test_a import load as aload
from inspect import stack

def hello():
    print("test_xxxxxxx2222")
    frameinfo = stack()[2]
    print(frameinfo)
    print("test_xxxxxxx2222")

def load():
    print("xxxxxx")
    aload()
    hello()
    print("xxxxxx")

