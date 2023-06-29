from typing import List, Optional, Type, Set

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy import Null

from .clipboard_item import ClipboardItem
from src.tnxts.util import _general_logger


class ORMSql:
    """数据库交互类

    使用orm框架与数据库进行交互，可以适应不同类型的数据库
    """

    def __init__(self):
        self.engine = None
        self.session = None
        self._init_connet()

    def _init_connet(self):
        try:
            self.engine = create_engine('mysql+pymysql://root:root@localhost:3306/clipboard_db?charset=utf8mb4')
            self.session = sessionmaker(bind=self.engine)
        except Exception as ex:
            _general_logger.logger.error(ex)
            

    def _connect(self) -> Session:
        try:
            return self.session()
        except Exception as ex:
            _general_logger.logger.error(ex)
            

    
    def _disconnect(self, session):
        session.close()

    
    def delete(self, filter: Set) -> int:
        """
        根据filter删除clipboard_item
        :param filter:
        :return:
        """
        session: Optional[Session] = None
        try:
            session = self._connect()

            d = session.query(ClipboardItem).filter(*filter).delete()

            session.commit()
            return d
        except Exception as ex:
            if session:
                session.rollback()
            _general_logger.logger.error(ex)

        finally:
            if session:
                session.close()
        return 0

    
    def insert(self, item: Type[ClipboardItem]) -> bool:
        """
        插入clipboard_item
        :param item:
        :return:
        """
        session: Optional[Session] = None
        try:
            session = self._connect()

            session.add(item)
            session.commit()
            return True
        except Exception as ex:
            if session:
                session.rollback()
            _general_logger.logger.error(ex)

        finally:
            if session:
                session.close()
        return False

    
    def select(self, filter: Set) -> List[ClipboardItem]:
        """
        根据filter查找clipboard_item
        :param filter:
        :return:
        """
        session: Optional[Session] = None
        try:
            session = self._connect()

            d = session.query(ClipboardItem).order_by(ClipboardItem.priority.desc()).order_by(
                ClipboardItem.create_time.desc()).filter(*filter).all()

            return d
        except Exception as ex:
            if session:
                session.rollback()
            _general_logger.logger.error(ex)

        finally:
            if session:
                session.close()

    
    def update(self, filter, update):
        """
        插入clipboard_item
        :param item:
        :return:
        """
        session: Optional[Session] = None
        try:
            session = self._connect()

            update_statement = {getattr(ClipboardItem, field): value for field, value in update.items()}

            session.query(ClipboardItem).filter(*filter).update(update_statement)
            session.commit()
            return True
        except Exception as ex:
            if session:
                session.rollback()
            _general_logger.logger.error(ex)

        finally:
            if session:
                session.close()
        return False

    
    def all(self) -> list[Type[ClipboardItem]]:
        """
        返回所有的clipboard_item
        :return:
        """
        session: Optional[Session] = None
        try:
            session = self._connect()

            d = session.query(ClipboardItem).order_by(ClipboardItem.priority.desc()).order_by(
                ClipboardItem.create_time.desc()).all()

            return d
        except Exception as ex:
            if session:
                session.rollback()
            _general_logger.logger.error(ex)

        finally:
            if session:
                session.close()

    def all_collection(self) -> List[ClipboardItem]:
        """
        返回所有的collection
        :return:
        """
        session: Optional[Session] = None
        try:
            session = self._connect()

            filter = {
                ClipboardItem.collect_time != None
            }

            d = session.query(ClipboardItem).filter(*filter).order_by(ClipboardItem.priority.desc()).order_by(ClipboardItem.collect_time.desc()).all()


            return d
        except Exception as ex:
            if session:
                session.rollback()
            _general_logger.logger.error(ex)

        finally:
            if session:
                session.close()


_sql = ORMSql()
