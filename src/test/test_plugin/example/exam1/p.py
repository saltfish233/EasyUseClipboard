from src.tnxts.plugin.loader import load_plugin,load_plugins
import pkgutil

def hellop():
    print("i m p")

q = load_plugin("src.tnxts.test.test_plugin.example.exam1.exam2.q.py")