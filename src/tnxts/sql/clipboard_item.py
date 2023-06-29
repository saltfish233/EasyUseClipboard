from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer,BIGINT,TEXT,VARCHAR,TIMESTAMP,BOOLEAN

_base = declarative_base()
class ClipboardItem(_base):
    """剪贴板item的sql对象

    """
    __tablename__ = 'tb_clipboard_item'
    id = Column(BIGINT,primary_key=True)
    data = Column(TEXT,nullable=False)
    title = Column(VARCHAR(1000))
    type = Column(VARCHAR(50))
    process = Column(VARCHAR(100))
    create_time = Column(TIMESTAMP,nullable=False)
    last_use_time = Column(TIMESTAMP)
    last_edit_time = Column(TIMESTAMP)
    collect_time = Column(TIMESTAMP)
    use_count = Column(Integer,nullable=False,default=0)
    priority = Column(Integer,nullable=False,default=0)
    is_visible = Column(BOOLEAN,nullable=False,default=True)
