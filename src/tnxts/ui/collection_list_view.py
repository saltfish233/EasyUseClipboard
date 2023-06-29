# coding:utf-8

import traceback

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem

from qfluentwidgets import ListWidget, RoundMenu, Action, MenuAnimationType, ListItemDelegate
from qfluentwidgets import FluentIcon as FIF

from src.tnxts.action import _collection,_clipboard
from src.tnxts.listener import _global_signal
from src.tnxts.util import _general_logger, dict_to_qmimedata
from src.tnxts.sql import ClipboardItem
from .component import LabelItem


class CustomDelegate(ListItemDelegate):
    """自定义delegate

    用于修改qlistwidgetitem的样式
    """

    def paint(self, painter, option, index):
        # 获取项的绘制区域
        rect = option.rect
        # 调整项的绘制区域，消除内边距
        rect.adjust(14, 2, 0, 4)
        # 将调整后的绘制区域传递给父类的 paint() 方法进行绘制
        option.rect = rect

        painter.setPen(QPen(Qt.gray, 0.5, Qt.SolidLine))
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())
        super().paint(painter, option, index)


class CollectionListView(QWidget):
    """剪贴板列表界面

    """

    def __init__(self):
        super(CollectionListView, self).__init__()
        self._initUi()

    @_general_logger.logger.catch()
    def _initUi(self):
        layout = QVBoxLayout()

        self.item_list = ListWidget(self)
        self.item_list.setContentsMargins(0, 0, 0, 0)
        self.item_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.item_list.setSpacing(0)

        delegate = CustomDelegate(self.item_list)
        self.item_list.setItemDelegate(delegate)

        id = 0
        for collection_item in _collection.items:
            data = dict_to_qmimedata(collection_item.data)
            item = QListWidgetItem()

            if data.hasImage():
                label_item = LabelItem(text=data.imageData(), index=id, item=collection_item,
                                       list_widget=self.item_list,mode=1)
            else:
                label_item = LabelItem(text=data.text(), index=id, item=collection_item,
                                       list_widget=self.item_list,mode=1)

            id += 1
            item.setData(Qt.UserRole, collection_item)
            item.setSizeHint(QSize(label_item.size().width(), label_item.size().height()))

            self.item_list.addItem(item)
            self.item_list.setItemWidget(item, label_item)

        _global_signal.collection_item_add.connect(lambda data: self.add_item(data))
        _global_signal.collection_item_del.connect(lambda item: self.delete_item(item['id']))
        _global_signal.collection_item_remove.connect(lambda item: self.remove_item(item['id']))

        self.item_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.item_list.customContextMenuRequested.connect(lambda x: self.item_list_menu(
            self.item_list.currentItem()
            if self.item_list.currentItem() is not None
            else None
        ))
        self.item_list.itemPressed.connect(lambda item: self.paste_item(item))

        layout.addWidget(self.item_list)
        self.setLayout(layout)

    def paste_item(self, item):
        try:
            item: LabelItem = self.item_list.itemWidget(item)
            if item.mouse_btn == Qt.LeftButton:
                _clipboard.paste(self.item_list.currentItem().data(Qt.UserRole))
        except Exception as ex:
            _general_logger.logger.error(ex)

    def add_item(self, collection_item: ClipboardItem):
        try:
            _collection.add_collection(collection_item)

            data = collection_item.data
            data = dict_to_qmimedata(data)

            item = QListWidgetItem()

            if data.hasImage():
                label_item = LabelItem(text=data.imageData(), index=0, item=collection_item,
                                       list_widget=self.item_list,mode=1)
            else:
                label_item = LabelItem(text=data.text(), index=0, item=collection_item,
                                       list_widget=self.item_list,mode=1)

            item.setData(Qt.UserRole, collection_item)
            item.setSizeHint(QSize(label_item.size().width(), label_item.size().height()))


            self.item_list.insertItem(0, item)
            self.item_list.setItemWidget(item, label_item)

        except Exception as ex:
            _general_logger.logger.error(ex)

    def remove_item(self,id):
        for i in range(self.item_list.count()):
            if self.item_list.item(i) is not None:
                item = self.item_list.item(i).data(Qt.UserRole)
                if item.id == id:
                    self.item_list.takeItem(self.item_list.row(self.item_list.item(i)))

    def delete_item(self, id):
        try:
            for i in range(self.item_list.count()):
                if self.item_list.item(i) is not None:
                    item = self.item_list.item(i).data(Qt.UserRole)
                    if item.id == id:
                        _collection.del_collection(item)
                        self.item_list.takeItem(self.item_list.row(self.item_list.item(i)))
                        _general_logger.logger.success(f"{item.id}已被取消收藏")

        except Exception as ex:
            _general_logger.logger.exception(ex)

    def item_list_menu(self, item):
        try:
            menu = RoundMenu(parent=self)

            uncollect_item_action = Action(FIF.HEART, "取消收藏")

            uncollect_item_data = {
                "id": self.item_list.currentItem().data(Qt.UserRole).id,
                "index": self.item_list.itemWidget(self.item_list.currentItem()).index
            }
            uncollect_item_action.triggered.connect(lambda: _global_signal.collection_item_del.emit(uncollect_item_data))

            menu.addAction(uncollect_item_action)

            menu.exec(QCursor.pos(), aniType=MenuAnimationType.DROP_DOWN)
        except Exception as ex:
            _general_logger.logger.error(ex)

