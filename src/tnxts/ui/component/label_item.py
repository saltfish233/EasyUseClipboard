# coding:utf-8


import re

from PyQt5 import sip
from PyQt5.QtCore import Qt, QSize, QByteArray
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy

from qfluentwidgets import ListWidget, StrongBodyLabel, PixmapLabel, BodyLabel,TitleLabel

from src.tnxts.listener import _global_signal
from src.tnxts.util import _general_logger



class LabelItem(QWidget):

    def __init__(self,text, index, item, list_widget: ListWidget,mode):
        super(LabelItem, self).__init__()
        self.index = index
        self.list_widget = list_widget
        self.item = item
        self.mouse_btn = -1
        self.mode = mode

        self._initUi(text)

    def _initUi(self,text):
        if isinstance(text,QImage) or isinstance(text,QByteArray) :
            qimg : QImage = QImage()
            if isinstance(text,QImage):
                qimg = text
            else:
                qimg.loadFromData(text)
            qimg = qimg.scaledToHeight(qimg.height() // 4)
            qimg = QPixmap.fromImage(qimg)

            self.content_label = PixmapLabel()
            self.content_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.content_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.content_label.setFixedHeight(qimg.height() * 2)
            self.content_label.setPixmap(qimg)
        else:
            self.text = re.sub('^(\t)*$\n', '', text, flags=re.MULTILINE)
            self.content_label = StrongBodyLabel()
            self.content_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.content_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.content_label.setFixedHeight(self.content_label.fontMetrics().height() * 3)
            self.content_label.setText(self.text)
            content_label_font = QFont("Microsoft YaHei", 10)
            content_label_font.setWeight(QFont.Normal)
            self.content_label.setFont(content_label_font)


        index_label_font = QFont("Microsoft YaHei", 10)
        index_label_font.setWeight(QFont.Normal)

        self.index_label = TitleLabel()
        self.index_label.setText(str(self.index + 1))
        self.index_label.setFont(index_label_font)
        self.index_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.index_label.setStyleSheet("color: gray;")
        # self.index_label.setStyleSheet("background-color: red;")
        self.index_label.setFixedSize(QSize(self.index_label.fontMetrics().width(str(self.index) + "  ", 100),
                                            self.content_label.height()))
        self.index_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.index_label.setContentsMargins(0, 0, 0, 0)


        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(self.content_label.height() + 10)
        self.setContentsMargins(0,0,0,0)
        # self.setStyleSheet("background-color: red;")

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.index_label)
        layout.addWidget(self.content_label)
        layout.setAlignment(Qt.AlignVCenter)

        self.setLayout(layout)

        if  self.mode == 0:
            _global_signal.clipboard_item_add.connect(lambda item: self.increase_index(item))
            _global_signal.clipboard_item_delete.connect(lambda item: self.decrease_index(item['index']))
        elif self.mode == 1:
            _global_signal.collection_item_add.connect(lambda item: self.increase_index(item))
            _global_signal.collection_item_del.connect(lambda item: self.decrease_index(item['index']))
            _global_signal.collection_item_remove.connect(lambda item: self.decrease_index(item['index']))

    def increase_index(self,item):
        try:
            if not sip.isdeleted(self.index_label):
                self.index += 1
                self.index_label.setText(str(self.index + 1))
        except Exception as ex:
            _general_logger.logger.error(ex)

    
    def decrease_index(self, base_index):
        try:
            if not sip.isdeleted(self.index_label):
                if self.index > base_index:
                    self.index -= 1
                    self.index_label.setText(str(self.index + 1))
        except Exception as ex:
            _general_logger.logger.error(ex)

    
    def mousePressEvent(self, e):
        try:
            if e.buttons() == Qt.LeftButton:
                self.mouse_btn = Qt.LeftButton
            elif e.buttons() == Qt.RightButton:
                self.mouse_btn = Qt.RightButton
            elif e.buttons() == Qt.MidButton:
                self.mouse_btn = Qt.MidButton
        except Exception as ex:
            _general_logger.logger.error(ex)

        super().mousePressEvent(e)

    
    def mouseReleaseEvent(self, e):
        try:
            parent = self.parent().parent()
            parent.parent().item_list.itemClicked.emit(parent.currentItem())

            super().mouseReleaseEvent(e)
        except Exception as ex:
            _general_logger.logger.error(ex)

    
    def enterEvent(self, event):
        try:
            self.parent().parent()._setHoverRow(self.index)
        except Exception as ex:
            _general_logger.logger.error(ex)