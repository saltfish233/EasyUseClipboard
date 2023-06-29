from typing import Optional

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from qfluentwidgets import ListWidget, SwitchButton

from src.tnxts.util import _general_logger


class SwitchableItem(QWidget):

    
    def __init__(self,text: Optional[str],index, plugin,list_widget: ListWidget):
        super(SwitchableItem, self).__init__()

        self.index = index
        self.list_widget = list_widget
        self.plugin = plugin

        content = QLabel(text)
        button = SwitchButton()
        button.setOffText("")
        button.setOnText("")
        button.checkedChanged.connect(lambda x : self.set_plugin_enable(x))

        layout = QHBoxLayout()
        layout.addWidget(content)
        layout.addStretch(1)
        layout.addWidget(button)

        self.setLayout(layout)

    
    def enterEvent(self, event):
        try:
            self.parent().parent()._setHoverRow(self.index)
        except Exception as ex:
            _general_logger.get_logger().error(ex)
    def set_plugin_enable(self, enable: bool):
        self.plugin.enable = enable