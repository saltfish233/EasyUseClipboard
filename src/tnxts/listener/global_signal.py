from PyQt5.QtCore import QObject, pyqtSignal

from src.tnxts.sql import ClipboardItem


class GlobalSignal(QObject):
    """全局信号

    """
    paste = pyqtSignal(str)
    copy = pyqtSignal(str)
    clipboard_item_add = pyqtSignal(ClipboardItem)
    clipboard_item_delete = pyqtSignal(dict)
    collection_item_add = pyqtSignal(ClipboardItem)
    collection_item_del = pyqtSignal(dict)
    collection_item_remove = pyqtSignal(dict)

_global_signal = GlobalSignal()