import pickle
import base64
from typing import Dict

from PyQt5.QtCore import QMimeData, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QImage

from .log import _general_logger



def obj_to_base64(obj: object) -> str:
    """
    object转base64
    :param obj:
    :return:
    """

    o = pickle.dumps(obj)
    obj_bytes = base64.b64encode(o)
    return obj_bytes.decode('utf8')


def base64_to_dict(src: str) -> dict:
    """
    base64转dict
    :param src:
    :return:
    """

    src = src.encode('utf8')
    obj_bytes = base64.b64decode(src)
    obj = pickle.loads(obj_bytes)
    return dict(obj)


def _qmimedata_to_dict( data: QMimeData, available_formats) -> Dict:
    """
    qmimedata转dict
    :param data:
    :param available_formats:
    :return:
    """
    d: Dict = {}

    for format in available_formats:
        d[format] = data.data(format)

    d['imageData'] = ''
    if data.hasImage():
        d['imageData'] = qimage_to_base64(data.imageData())

    return d


def dict_to_qmimedata(data: Dict) -> QMimeData:
    """
    dict转qmimedata
    :param data:
    :return:
    """

    d: QMimeData = QMimeData()

    for format in data.keys():
        if format == "imageData":
            continue
        d.setData(format, data[format])

    try:
        if data['imageData'] != '':
            d.setImageData(base64_to_qimage(data['imageData']))
    except:
        pass

    return d


def qimage_to_base64(qimage: QImage):
    # 将QImage转换为QByteArray
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, "PNG")  # 可以选择不同的图像格式，如PNG、JPEG等
    buffer.close()

    # 将QByteArray编码为Base64字符串
    base64_str = base64.b64encode(byte_array).decode("utf-8")
    return base64_str


def base64_to_qimage(base64_str):
    """
    base64转qimage
    :param base64_str:
    :return:
    """

    # 将Base64字符串解码为字节数据
    byte_data = base64.b64decode(base64_str)
    byte_array = QByteArray(byte_data)
    qimage = QImage.fromData(byte_array)

    return qimage


def is_mime_data_equal(mime_data1, mime_data2):
    """
    判断两个mimedata是否相同
    :param mime_data1:
    :param mime_data2:
    :return:
    """

    # 获取两个QMimeData对象的MIME格式列表
    formats1 = mime_data1.formats()
    formats2 = mime_data2.formats()

    # 检查MIME格式列表是否相同
    if formats1 != formats2:
        return False

    # 逐个检查MIME格式对应的数据是否相同
    for format in formats1:
        data1 = mime_data1.data(format)
        data2 = mime_data2.data(format)
        if data1 != data2:
            return False

    # 所有MIME格式和对应的数据都相同
    return True