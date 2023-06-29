from src.tnxts.sql.clipboard_item import ClipboardItem
from src.tnxts.sql.ormsql import _sql
from src.tnxts.util import now, _general_logger, base64_to_dict


class Collection():

    def add_collection(self, item: ClipboardItem):
        """
        收藏item
        :param item:
        :return:
        """
        try:
            item.collect_time = now()
            filter = {
                ClipboardItem.id == item.id
            }
            update = {
                "collect_time" : item.collect_time
            }
            _sql.update(filter, update)
        except Exception as ex:
            _general_logger.logger.error(ex)

    def del_collection(self,item: ClipboardItem):
        """
        取消收藏item
        :param item:
        :return:
        """
        try:
            item.collect_time = None
            filter = {
                ClipboardItem.id == item.id
            }
            update = {
                "collect_time": None
            }
            _sql.update(filter, update)
        except Exception as ex:
            _general_logger.logger.error(ex)


    @property
    def items(self):
        """
        返回所有的collection
        :return:
        """
        try:
            l = []

            all = _sql.all_collection()
            if all is not None:
                for i in _sql.all_collection():
                    obj = base64_to_dict(i.data)
                    i.data = obj
                    l.append(i)

            return l
        except Exception as ex:
            _general_logger.logger.error(ex)


_collection = Collection()