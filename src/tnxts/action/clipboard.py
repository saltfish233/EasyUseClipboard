"""定义操作剪贴板的动作"""

from typing import List, Optional

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QMimeData

from keyboard import press_and_release

from src.tnxts.util import _general_logger, now, obj_to_base64, base64_to_dict, _qmimedata_to_dict, dict_to_qmimedata
from src.tnxts.sql import _sql,ClipboardItem

from src.tnxts.listener.window_listener import _window_listener
from src.tnxts.listener.global_signal import  _global_signal



class Clipboard:
    """剪贴板对象

    提供剪贴板操作能力
    """

    def __init__(self):
        self._is_clip_open: bool = False
        self.app = QApplication([])
        self.clipboard = self.app.clipboard()
        self.mimeData = self.clipboard.mimeData()
        self.previous_mimedata = None
        self.mouse_btn = -1

        self.initiative_paste = False

    @_general_logger.logger.catch()
    def current_content(self):
        """获取当前剪贴板的内容"""
        return self.clipboard.mimeData()

    @property
    @_general_logger.logger.catch()
    def available_formats(self) -> List:
        """返回可用格式列表"""
        return self.mimeData.formats()

    @_general_logger.logger.catch()
    def set_mimedata(self,data: QMimeData):
        try:
            d = QMimeData()
            for format in self.available_formats:
                d.setData(format, data.data(format))

            if data.hasImage():
                d.setImageData(data.imageData())

            #会触发oncopy
            self.clipboard.blockSignals(True)
            self.clipboard.setMimeData(d)
            self.clipboard.blockSignals(False)

        except Exception as e:
            pass

    @_general_logger.logger.catch()
    def list(self) -> List:
        return list(_sql.all())

    @_general_logger.logger.catch()
    def remove(self, id: int):
        try:


            filter = {
                ClipboardItem.id == id
            }
            _sql.delete(filter)

            _general_logger.logger.success(str(id) +"已删除")
        except Exception as ex:
            pass

    @property
    @_general_logger.logger.catch()
    def items(self):
        l = []

        try:
            for i in  _sql.all():
                obj = base64_to_dict(i.data)
                i.data = obj
                l.append(i)
        except:
            pass

        return l

    def quick_store(self) -> bool:
        """快速存储剪贴板"""
        try:
            img_data: QImage

            if self.initiative_paste is True:
                self.initiative_paste = False
                return False

            clipboard_data = _clipboard.current_content()

            ctime = now()

            dict_data = _qmimedata_to_dict(clipboard_data, self.available_formats)
            base64_data = obj_to_base64(dict_data)

            item = ClipboardItem()
            item.create_time = ctime
            item.data = base64_data

            _sql.insert(item)

            filter = {
                ClipboardItem.data == base64_data,
                ClipboardItem.create_time == ctime
            }
            data = _sql.select(filter)
            if data:
                data[0].data = dict_data
                _global_signal.clipboard_item_add.emit(data[0])
                _general_logger.logger.success(clipboard_data.text() + "\n已存入剪贴板")
        except Exception as ex:
            _general_logger.logger.error(ex)
            return False
        return True

    
    def read_stroage(self):
        print(_sql.all())

    @_general_logger.logger.catch()
    def paste(self, item: Optional[ClipboardItem] = None):
        try:
            data = dict_to_qmimedata(item.data)

            if data:
                self.initiative_paste = True
                self.set_mimedata(data)


            _window_listener.previous_window.activate()
            press_and_release("ctrl+v")
        except Exception as e:
            pass


    def cache(self):
        pass

    
    def _to_pic(self, data: bytes) :
        pass

_clipboard = Clipboard()