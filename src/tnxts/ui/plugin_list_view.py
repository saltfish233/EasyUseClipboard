# coding:utf-8

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem

from qfluentwidgets import ListWidget, RoundMenu,Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF

from src.tnxts.plugin import _plugins
from src.tnxts.util import _general_logger
from .component import SwitchableItem




class PluginListView(QWidget):
    """插件列表界面

    """

    @_general_logger.logger.catch()
    def __init__(self):
        super(PluginListView, self).__init__()

        layout = QVBoxLayout()

        self.item_list = ListWidget(self)

        i = 0
        for plugin in _plugins.values():
            item = QListWidgetItem()
            # item = SwitchableItem()
            item.setData(Qt.UserRole, plugin)
            if plugin.metadata:
                switch_item = SwitchableItem(plugin.metadata.name, i,plugin,self.item_list)
            else:
                switch_item = SwitchableItem(plugin.name, i, plugin ,self.item_list)
            i += 1

            item.setSizeHint(QSize(100, 50))

            self.item_list.addItem(item)
            self.item_list.setItemWidget(item, switch_item)

        layout.addWidget(self.item_list)
        self.setLayout(layout)



    def item_list_menu(self,item):
        menu = RoundMenu(parent=self)

        # add actions
        menu.addAction(Action(FIF.COPY, '复制'))
        menu.addAction(Action(FIF.PASTE, '粘贴'))
        menu.addAction(Action(FIF.DELETE, '删除'))

        menu.exec(QCursor.pos(), aniType=MenuAnimationType.DROP_DOWN)