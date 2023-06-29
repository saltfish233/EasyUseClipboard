from src.tnxts.action import _clipboard
from src.tnxts.listener.global_signal import _global_signal
from src.tnxts.plugin import _module_name_to_plugin
from src.tnxts.util import _general_logger


class ClipboardListener:
    """剪贴板监听器

    """


    def __init__(self):
       self.on_copy(_clipboard.quick_store)

    def on_copy(self, func):
        """复制事件"""
        _clipboard.clipboard.dataChanged.connect(lambda : self.decorator(func))
        # _clipboard.clipboard.dataChanged.connect(func)
        # global_signal.copy.connect(func)

    def on_paste(self,func):
        """粘贴事件"""
        _global_signal.paste.connect(func)

    def decorator(self, func, **args):
        try:
            plugin = _module_name_to_plugin(func.__module__)

            if plugin and plugin.enable:
                func()
        except Exception as ex:
            _general_logger.logger.error(ex)
        if func.__name__ == "quick_store":
            func()




clipboard_listener = ClipboardListener()