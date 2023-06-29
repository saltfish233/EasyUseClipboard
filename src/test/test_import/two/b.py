from importlib import import_module

a = import_module(r"src.tnxts.test.test_import.two.a")
print(a.__name__)

