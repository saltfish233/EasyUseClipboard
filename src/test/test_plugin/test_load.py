from src.tnxts.plugin.loader import load_plugin,load_plugins
import pkgutil
from pathlib import Path
from importlib import import_module

def test_load_plugin():
    a = load_plugins("src.tnxts.test.test_plugin.example")
    # a.module.hello()
    print(f"获取到集合{a}")

test_load_plugin()