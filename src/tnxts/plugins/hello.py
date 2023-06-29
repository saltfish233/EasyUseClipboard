from src.tnxts.listener import _clipboard_listener
from src.tnxts.plugin import PluginMetadata

_metadata = PluginMetadata(
    name="helloworld",
    author="Tnxts",
    description="在复制时输出hello, world",
    usage="复制时自动运行"
)

def print_hello():
    print("hello, world")

_clipboard_listener.on_copy(print_hello)