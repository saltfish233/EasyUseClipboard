# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel

from qfluentwidgets import Pivot, RoundMenu,Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF

from src.tnxts.util import _general_logger
from .clipboard_list_view import ClipboardListView
from .plugin_list_view import PluginListView
from .collection_list_view import CollectionListView

class MainWindow(QWidget):
    """主界面

    """
    def __init__(self):
        super().__init__()

        self.clipboard_index = 0
        self.love_index = 1
        self.plugin_index = 2



        # setTheme(Theme.DARK)
        self.setStyleSheet("""
            MainWindow{background: white}
            QListWidgetItem{
                 font: 20px 'Segoe UI';
            }
        """)
        self.resize(400, 500)

        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.clipboard_list_view = ClipboardListView()
        self.collection_list_view = CollectionListView()
        self.plugin_list_view = PluginListView()



        self.stackedWidget.setContentsMargins(0,0,0,0)
        self.addSubInterface(self.clipboard_list_view, 'songInterface', '剪贴板')
        self.addSubInterface(self.collection_list_view, 'albumInterface', '收藏')
        self.addSubInterface(self.plugin_list_view, 'artistInterface', '插件')



        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignHCenter)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.setLayout(self.vBoxLayout)

        # self.setContentsMargins(0, 0, 0, 0)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.clipboard_list_view)
        self.pivot.setCurrentItem(self.clipboard_list_view.objectName())

    
    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    
    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())

    
    def item_list_menu(self,item):
        print(item)
        menu = RoundMenu(parent=self)

        menu.addAction(Action(FIF.HEART, '收藏'))
        menu.addSeparator()
        menu.addAction(Action(FIF.DELETE, '删除'))

        menu.exec(QCursor.pos(), aniType=MenuAnimationType.DROP_DOWN)