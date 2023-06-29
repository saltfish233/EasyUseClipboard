import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.tnxts.listener import _window_thread, _keyboard_thread
from src.tnxts.ui import MainWindow
from src.tnxts.plugin.loader import load_plugin

def init():
    initPlugin()
    initThread()
    initUi()


def initPlugin():
    load_plugin("src.tnxts.plugins.hello.py")

def initThread():
    _window_thread.start()
    _keyboard_thread.start()

def initUi():
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("EasyUseClipboard")
    w.show()
    app.exec_()

init()