from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, ForeignKey, JSON, INT, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from database import Base


class TimestampMixin(object):
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)


class DBResource(Base, TimestampMixin):
    __tablename__ = 'db_resources'

    id = Column(CHAR(36), primary_key=True)
    resource_name = Column(String(100))
    resource_type = Column(Enum('Database', 'Table', 'System', name='resource_type'), nullable=False)
    resource_comment = Column(CHAR(100))
    system_id = Column(CHAR(36), ForeignKey('db_resources.id', ondelete='cascade'), nullable=True, default=None)
    database_id = Column(CHAR(36), ForeignKey('db_resources.id', ondelete='cascade'), nullable=True, default=None)
    extra = Column(JSON, nullable=True)

    system = relationship('DBResource', foreign_keys=[system_id], cascade="all,delete", passive_deletes=True)
    database = relationship('DBResource', foreign_keys=[database_id], cascade="all,delete", passive_deletes=True)


class DataDirectory(Base, TimestampMixin):
    __tablename__ = 'data_directories'

    id = Column(CHAR(36), primary_key=True)
    system_id = Column(CHAR(36), ForeignKey('db_resources.id', ondelete='cascade'))
    db_id = Column(CHAR(36), ForeignKey('db_resources.id', ondelete='cascade'))
    table_id = Column(CHAR(36), ForeignKey('db_resources.id', ondelete='cascade'))
    entry_name = Column(String(255), nullable=False)
    comment = Column(Text)
    entry_length = Column(INT, nullable=False)
    entry_type = Column(CHAR(100))
    entry_name_chn = Column(CHAR(100))
    extra = Column(JSON, nullable=True)

    system = relationship('DBResource', foreign_keys=[system_id], cascade="all,delete", passive_deletes=True)
    database = relationship('DBResource', foreign_keys=[db_id], cascade="all,delete", passive_deletes=True)
    table = relationship('DBResource', foreign_keys=[table_id], cascade="all,delete", passive_deletes=True)
