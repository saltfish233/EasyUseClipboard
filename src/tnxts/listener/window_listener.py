from typing import Optional

from PyQt5.QtCore import QThread

from time import sleep
from pygetwindow import Win32Window
import pyautogui

from src.tnxts.util import _general_logger


class WindowListener:
    """窗口监听器

    """

    def __init__(self):
        self.current_window : Win32Window = None
        self.previous_window : Win32Window = None
        self.update_current_window()

    @property
    def _program_window(self) -> Optional[Win32Window]:
        if pyautogui.getWindowsWithTitle("EasyUseClipboard"):
            return pyautogui.getWindowsWithTitle("EasyUseClipboard")[0]
        return None

    
    def update_current_window(self):
        tmp = pyautogui.getActiveWindow()
        if tmp != None and tmp != self.current_window:
            self.previous_window = self.current_window
            if tmp != self._program_window:
                self.current_window = tmp


class WindowListenerThread(QThread):
    def __init__(self):
        super(WindowListenerThread, self).__init__()

    
    def run(self) -> None:
        while True:
            _window_listener.update_current_window()
            sleep(0.1)


_window_listener = WindowListener()
_window_thread = WindowListenerThread()