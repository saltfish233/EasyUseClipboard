from src.tnxts.plugin.loader import load_plugin,load_plugins
import pkgutil

def hello():
    print("hello im a")

# b = load_plugin("src.tnxts.test.test_plugin.example.b.py")

p = load_plugin("src.tnxts.test.test_plugin.example.exam1.p.py")
